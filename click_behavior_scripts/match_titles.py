def get_id_to_title_dict():
    print(f"Loading imports...")
    import pandas as pd

    print("Loading dataset titles...")

    news_file = "news.xlsx"
    news_path = f"/mnt/c/Users/cchase/Documents/MIND/{news_file}"

    df = pd.read_excel(news_path)#, sep='\t')
    df.columns = ['newsID', 'Category', 'SubCategory','Title', 'Abstract', 'URL', 'Title Entities', 'Abstract Entites']

    newsIDs = list(df["newsID"])
    titles = list(df["Title"])

    input_file = "75000/How_many_times_'clicked_article'_was_clicked_when_'click_hist_article'_was_in_user's_history.txt"
    input_path = f"/mnt/c/Users/cchase/Documents/CS_497_R/click_behavior_scripts/out/{input_file}"

    #print(f"ids: {newsIDs[:10]}")
    #print(f"titles: {titles[:10]}")

    id_to_title = {}

    for i in range(len(newsIDs)):
        id_to_title[newsIDs[i]] = titles[i]

    return id_to_title
