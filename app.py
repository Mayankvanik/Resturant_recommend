from flask import Flask,render_template
from flask import request
import pandas as pd
import  numpy as np
import pickle


popular_40 = pd.read_csv('zomato_40.csv')
df = pd.read_csv('df.csv')
df1 = df.set_index('resturant')
cosine = pickle.load(open('similarity.pkl','rb'))

app =  Flask(__name__)



@app.route('/')
# def index():
#     return render_template('index.html')
def index():
    return render_template('index.html',
                           restaurant_detail_url=list(popular_40['site_url'].values),
                           img_url=list(popular_40['image'].values),
                           restro_name = list(popular_40['resturant'].values),
                           rate=list(popular_40['rate'].values),
                           sector=list(popular_40['sector'].values),
                           food=list(popular_40['food'].values),
                           price=list(popular_40['avg_price_for_two'].values))

@app.route('/home')
def home1():
    return render_template('index.html',
                           restaurant_detail_url=list(popular_40['site_url'].values),
                           img_url=list(popular_40['image'].values),
                           restro_name = list(popular_40['resturant'].values),
                           rate=list(popular_40['rate'].values),
                           sector=list(popular_40['sector'].values),
                           food=list(popular_40['food'].values),
                           price=list(popular_40['avg_price_for_two'].values))

@app.route('/perform_registration', methods=['POST'])
def perform_registration():
    nam = request.form.get('restroName')
    nam = str(nam)

    index = np.where(df.resturant == nam)[0][0]
    items = sorted(list(enumerate(cosine[index])), key=lambda x: x[1], reverse=True)[0:6]
    #return str(items)
    data = []

    for i in items:
        li = []
        temp_df = df[df.resturant == df1.index[i[0]]]
        li.extend(list(temp_df['resturant'].values))
        li.extend(list(temp_df['sector'].values))
        li.extend(list(temp_df['rate'].values))
        li.extend(list(temp_df['food'].values))
        li.extend(list(temp_df['avg_price_for_two'].values))
        li.extend(list(temp_df['image'].values))
        # Add other data you want to collect here
        data.append(li)

    return render_template('recommend.html', data=data)

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    selected_options = request.form.getlist('user_input[]')
    selected_price = request.form.getlist('price_range')

    split_values = selected_price[0].split('-')
    # Convert the resulting strings to integers
    start_range = int(split_values[0])
    end_range = int(split_values[1])

    #print(start_range, end_range)
    top_15=df[(df.fod.str.contains('|'.join(selected_options),case=False))&(df.avg_price_for_two.between(start_range,end_range))].sort_values('rate_ratio', ascending=False)
    return render_template('select_food.html',
                           food_item=selected_options,
                           restaurant_detail_url=list(top_15['image'].values),
                           img_url=list(top_15['image'].values),
                           restro_name=list(top_15['resturant'].values),
                           rate=list(top_15['rate'].values),
                           sector=list(top_15['sector'].values),
                           food=list(top_15['food'].values),
                           price=list(top_15['avg_price_for_two'].values))


if __name__ == '__main__':
    app.run(debug=True)


