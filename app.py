from flask import Flask,render_template,request,redirect,url_for
import pickle
import uuid
import os


app = Flask(__name__)



@app.route('/',methods=['POST','GET'])
def index():
    try:
        with open('static/items.txt','rb') as h:
            items = pickle.load(h)
    except:
        items = []
    
    group_items = [items[i:i+3] for i in range(0,len(items),3)]
    
    #additems
    if(request.method == 'POST'):
        form = request.form
        name = form['name']
        desc = form['desc']
        img = request.files['file']
        # print(form)
        img_path = os.path.join('static/image',img.filename)
        img.save(img_path)
        item = {'id' : str(uuid.uuid4()),'name':name ,'desc':desc,'img':img_path}
        items.append(item)
        with open('static/items.txt','wb') as h:
            items = pickle.dump(items,h)
        with open('static/items.txt','rb') as h:
            items = pickle.load(h)
        group_items = [items[i:i+3] for i in range(0,len(items),3)]
    else:
        group_items = [items[i:i+3] for i in range(0,len(items),3)]
        
    return render_template('index.html',items2=group_items)

@app.route('/delete/<id>',methods=['DELETE'])
@app.route('/delete',methods=['POST'])
def delete(id=None):
    with open('static/items.txt','rb') as h:
            items = pickle.load(h)
    if(request.method == "POST"):
        selected_items = request.form.getlist('multiitems')
        print(selected_items)
        
        for i in selected_items:
            item = eval(i)                 #eval() แปลง str เป็น type เดิม
            items.remove(item)
        
        with open('static/items.txt','wb') as h:
            items = pickle.dump(items,h)
    elif request.method == "DELETE":
        print(id)
        item = [i for i in items if i['id'] == id][0]
        items.remove(item)
        with open('static/items.txt','wb') as h:
            items = pickle.dump(items,h)
        return url_for('index')
            
    return redirect(url_for('index'))

@app.route('/item/<id>',methods = ['POST','GET'])
def about_item(id):
    with open('static/items.txt','rb') as h:
        items = pickle.load(h)
        
        
    if request.method == "POST":
        form = request.form
        name = form['name']
        desc = form['desc']
        img = request.files['file']
        item = [i for i in items if i['id'] == id][0]
        # print(form)
        if img:
            img_path = os.path.join('static/image',img.filename)
            img.save(img_path)
            item['img'] = img_path

        item['name'] = name
        item['desc'] = desc
        
        with open('static/items.txt','wb') as h:
            items = pickle.dump(items,h)
        
        
    else:
        item = [i for i in items if i['id'] == id][0]
        print(item)
    return render_template('item.html',item=item)

if __name__ == "__main__":
    app.run(debug=True)
    