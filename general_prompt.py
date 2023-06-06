import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

general_prompt_tempalte ="""
Here are the general information of our store:
Our store name is {name} and located at {location}. And our sales data collected from Doordash like : {sales}. And our review summary collected by Doordash like : {review}

When compare with other stores, we collect data from doordash, we honor following metrics based on priority scores. Here are metrics data for our store: {metrics}

When makeing suggestions, please uses below data as priority:
improve inflation : {inflation_rec}
improve photo coverage : {photo_rec}
improve menu variety: {menu_rec}
improve promotion adoption : {promo_rec}
improve ads adoption : {ads_rec}
Below are some compatitors metrics data for references: {compatitors}
"""

def build_general_insights_prompt(json_data):
    location = json_data["storeDetails"]["location"]
    name = json_data["storeDetails"]["name"]
    sales_data = json_data["generalCompsAnalysis"]["sales"]
    review_data = json_data["generalCompsAnalysis"]["reviewComparison"]
    metrics = json_data["IndividualCompetitorAnalysis"]["metrics"]
    compatitors = json_data["IndividualCompetitorAnalysis"]["comps"]
    inflation_rec = json_data["IndividualCompetitorAnalysis"]["metrics"]["inflationRate"]["recommendedActions"]
    photo_rec = json_data["IndividualCompetitorAnalysis"]["metrics"]["photoCoverage"]["recommendedActions"]
    menu_rec = json_data["IndividualCompetitorAnalysis"]["metrics"]["menuVariety"]["recommendedActions"]
    promo_rec = json_data["IndividualCompetitorAnalysis"]["metrics"]["promotionAdoption"]["recommendedActions"]
    ads_rec = json_data["IndividualCompetitorAnalysis"]["metrics"]["AdsAdoption"]["recommendedActions"]
    return general_prompt_tempalte.format(
        name = name,
        location = location,
        sales = sales_data,
        review = review_data,
        metrics = metrics,
        inflation_rec = inflation_rec,
        photo_rec = photo_rec,
        menu_rec = menu_rec,
        promo_rec = promo_rec,
        ads_rec = ads_rec,
        compatitors = compatitors)

def get_insights_json():
    # dummy response from upstream dependencies
    file_path = "utils/sampleUpstreamResponse.json"
    with open(file_path) as file:
        data = json.load(file)
        return data
