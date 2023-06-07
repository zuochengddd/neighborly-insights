import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

general_prompt_tempalte ="""
Here are the general information of our store:
Our store detail info : {store_details}.
Our store sales info : {store_sales}.
Our store doordash reviews : {store_reivews}.
Our store neighborly insight metrics info: {store_metrics}
"""

def build_general_insights_prompt(json_data):

    store_details = build_store_details_prompt(json_data)
    
    store_sales = build_store_sales_prompt(json_data)

    store_review = build_store_review_prompt(json_data)

    store_metrics = build_store_metrics_prompt(json_data)

    return general_prompt_tempalte.format(
        store_details = store_details,
        store_sales = store_sales,
        store_reivews = store_review,
        store_metrics = store_metrics
    )

def build_store_details_prompt(json_data): 
    prompt = ""
    store_details_prompt_template = """
    Our store is located at {address}, {city}, {state}, and is named {name}.
    Our nearby stores are:
    """
    location = json_data["storeDetails"]["location"]
    name = json_data["storeDetails"]["name"]

    our_store = store_details_prompt_template.format(
        name = name,
        address = location["address"],
        city = location["city"],
        state = location["state"]
    )
    
    prompt = prompt + our_store
    nearby_stores_template = """
    Store name: {name}, Address: {address}, {city}, {state}, and similarity score compared to our store: {score}.
    """

    nearby_stores = json_data["IndividualCompetitorAnalysis"]["comps"]
    for store in nearby_stores:
        prompt = prompt + nearby_stores_template.format(
            name = store["storeDetails"]["name"],
            address = store["storeDetails"]["location"]["address"],
            city = store["storeDetails"]["location"]["city"],
            state = store["storeDetails"]["location"]["state"],
            score = store["similarityScore"]
        )
    return prompt

def build_store_sales_prompt(json_data):
    prompt = """
    In last quarter, Here are the our sales data for each category compared to neighbors stores:
    """
    store_sales_prompt_template = """
    For category {category}, our sales is ${sale_amount} while average neighbors sale is ${sale_average}, our sould amount is {sold_amount} while average neighbors sold amount is {sold_mount_average}.
    """
    sales = json_data["generalCompsAnalysis"]["sales"]
    for sale in sales:
        prompt = prompt + store_sales_prompt_template.format(
            category = sale["category"],
            sale_amount = sale["mySalePastQuarter"],
            sale_average = sale["averageNeighborsSale"],
            sold_amount = sale["soldAmount"],
            sold_mount_average = sale["averageNeighborSoldAmount"],
        )
    return prompt

def build_store_review_prompt(json_data):
    store_review_prompt_template = """
    Our store has a rating of {rating} compared to average neighbor rating {average_rating}. And the top liked review mentioned {most_liked} while top disliked review mentioned {disliked}.
    """
    reviews = json_data["generalCompsAnalysis"]["reviews"]
    return store_review_prompt_template.format(
        rating = reviews["rating"],
        average_rating = reviews["averageNeighborRating"],
        most_liked = reviews["most_liked"],
        disliked = reviews["most_disliked"]
    )

def build_store_metrics_prompt(json_data):
    prompt = """
    Below are the metrics analysis data for the stores comparison. When we need to evealute and analysis the our store data with others, we will evaulate prioritze the metrics based on priority scores in decending orders.
    """
    store_metrics_prompt_template = """
    For metric {metric}, the priority score is {priority_score}, value is {value}. If an recommendation is needed to improve this metric, suggest user like: {improvement}, please also convert this {link} to an HTML URL link in resonse, otherwise, encourage user to keep the good work, like: {encouragement}.
    """

    metrics = json_data["IndividualCompetitorAnalysis"]["metrics"]

    for metric in metrics:
        prompt = prompt + store_metrics_prompt_template.format(
            metric = metric["name"],
            value = metric["value"],
            priority_score = metric["priorityScore"],
            improvement = metric["recommendedActions"][0]["ImproventPrompt"],
            encouragement = metric["recommendedActions"][0]["EncouragementPrompt"],
            link = metric["recommendedActions"][0]["link"]
        )

    prompt = prompt + """
    Below are metrics summary of other competitors stores:
    """
    other_stores = json_data["IndividualCompetitorAnalysis"]["comps"]

    other_store_metrics_summary = """
    For store: {store}, the inflationRate data is {inflation}, the photoCoverage data is {photoCoverage}, the menuVariety data is {menuVariety}, promotionAdoption rate is {promotionAdoption}, and adsAdoption rate is {adsAdoption}.
    """
    for store in other_stores:
        prompt = prompt + other_store_metrics_summary.format(
            store = store["storeDetails"]["name"],
            inflation = store["metrics"]["inflationRate"],
            photoCoverage = store["metrics"]["photoCoverage"],
            menuVariety = store["metrics"]["menuVariety"],
            promotionAdoption = store["metrics"]["promotionAdoption"],
            adsAdoption = store["metrics"]["adsAdoption"]
        )
    print(prompt)
    return prompt

def get_insights_json():
    # dummy response from upstream dependencies
    file_path = "utils/sampleUpstreamResponse.json"
    with open(file_path) as file:
        data = json.load(file)
        return data
