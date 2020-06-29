import datetime

from django.db import models
from django.utils import timezone

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import io
import urllib, base64

# For facets
from IPython.core.display import display, HTML
import base64
#!pip install facets-overview==1.0.0
from facets_overview.feature_statistics_generator import FeatureStatisticsGenerator


# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class  Chart(models.Model):
    title_text = models.CharField(max_length=200, default="dummy title")

    def __str__(self):
        return self.title_text

    @staticmethod
    def plot():
        x = np.arange(0, 5, 0.1)  
        y = np.sin(x)  
        plt.plot(x, y)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return uri

    @staticmethod    
    def describeData(fileName):
        df_1 = pd.DataFrame()
        df_1 = pd.read_csv(fileName,float_precision=4)
        return df_1.describe()

    @staticmethod    
    def generateStatsNotworking(df):
        fsg = FeatureStatisticsGenerator()
        dataframes = [
            {'table': df, 'name': 'trainData'}]
        censusProto = fsg.ProtoFromDataFrames(dataframes)
        protostr = base64.b64encode(censusProto.SerializeToString()).decode("utf-8")
        HTML_TEMPLATE = """<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
          <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">
          <facets-overview id="elem"></facets-overview>
          <script>
            document.querySelector("#elem").protoInput = "{protostr}";
          </script>"""
        html = HTML_TEMPLATE.format(protostr=protostr)
        return display(HTML(html))
        
    @staticmethod    
    def generateStats(df):
        fsg = FeatureStatisticsGenerator()
        dataframes = [
            {'table': df, 'name': 'trainData'}]
        censusProto = fsg.ProtoFromDataFrames(dataframes)
        protostr = base64.b64encode(censusProto.SerializeToString()).decode("utf-8")
        # HTML_TEMPLATE = """<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
        #   <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">
        #   <facets-overview id="elem"></facets-overview>
        #   <script>
        #     document.querySelector("#elem").protoInput = "{protostr}";
        #   </script>"""
        # html = HTML_TEMPLATE.format(protostr=protostr)
      
        return protostr
            
    @staticmethod    
    def displayFacets(fileName):
        df_1 = pd.DataFrame()
        df_1 = pd.read_csv(fileName,float_precision=4)
        str = Chart.generateStats(df_1)
        return str