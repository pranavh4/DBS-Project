from surplusfood import app, db
from flask import request
import traceback
import sys
from datetime import date, timedelta
from surplusfood.Database import DONATING_ORG, DONATION, DONATION_CONTAINS, DISTRIBUTOR, RECEIPT, RECEIPT_CONTAINS, RECEIVING_ORG, FOOD_ITEM

@app.route("/AddOrg", methods=['POST'])
def AddOrg():
    req = request.get_json()
    if "" in req.values():
        return {"status":-1}
        
    if req['type'] == 'Distributor':
        last_index = DISTRIBUTOR.query.all()
        if last_index:
            last_index = last_index[-1].Dist_id+1
        else:
            last_index=1
        org = DISTRIBUTOR(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            db.session.rollback()
            return {"status":-1}

    elif req['type'] == 'Donor':
        last_index = DONATING_ORG.query.all()
        if last_index:
            last_index = last_index[-1].Donor_id+1
        else:
            last_index=1
        org = DONATING_ORG(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            return {"status":-1}

    elif req['type'] == 'Reciever':
        last_index = RECEIVING_ORG.query.all()
        if last_index:
            last_index = last_index[-1].Receiver_id+1
        else:
            last_index=1
        org = RECEIVING_ORG(last_index,req['name'],req['address'],req['phone'],req['email'])
        try:
            db.session.add(org)
            db.session.commit()
            return {"status":1}
        except:
            return {"status":-1}


@app.route("/getDon", methods=['POST'])
def getDon():
    req = request.get_json()
    res={'donations':[]}
    if req['donor']=='':
        if req['dist']=='':
            res['donations'] = DONATION.query.all()
        else:
            res['donations'] = DONATION.query.filter_by(Dist_id=req['dist']).all()
    else:
        if req['dist']=='':
            res['donations'] = DONATION.query.filter_by(Donor_id=req['donor']).all()
        else:
            res['donations'] = DONATION.query.filter_by(Dist_id=req['dist'],Donor_id=req['donor']).all()
    for i in range(len(res['donations'])):
        print(DONATION_CONTAINS.Donation_id)
        foods = DONATION_CONTAINS.query.filter_by(Donation_id = res['donations'][i].Donation_id).all()
        print(foods[0].Food_id)
        for j in range(len(foods)):
            food_name = FOOD_ITEM.query.filter_by(Food_id=foods[j].Food_id).first().Food_name
            foods[j] = {'name':food_name,'quantity':foods[j].Amount}
        res['donations'][i] = {'id': res['donations'][i].Donation_id,'donor':res['donations'][i].Donor_id,'dist':res['donations'][i].Dist_id,'foods':foods,'date':res['donations'][i].Date}
    return res

@app.route("/getReciept", methods=['POST'])
def getReciept():
    req = request.get_json()
    res={'reciepts':[]}
    if req['reciever']=='':
        if req['dist']=='':
            res['reciepts'] = RECEIPT.query.all()
        else:
            res['reciepts'] = RECEIPT.query.filter_by(Dist_id=req['dist']).all()
    else:
        if req['dist']=='':
            res['reciepts'] = RECEIPT.query.filter_by(Receiver_id=req['reciever']).all()
        else:
            res['reciepts'] = RECEIPT.query.filter_by(Dist_id=req['dist'],Receiver_id=req['reciever']).all()
    for i in range(len(res['reciepts'])):
        foods = RECEIPT_CONTAINS.query.filter_by(Receipt_id = res['reciepts'][i].Receipt_id).all()
        for j in range(len(foods)):
            food_name = FOOD_ITEM.query.filter_by(Food_id=foods[j].Food_id).first().Food_name
            foods[j] = {'name':food_name,'quantity':foods[j].Amount}
        res['reciepts'][i] = {'id': res['reciepts'][i].Receipt_id,'reciever':res['reciepts'][i].Receiver_id,'dist':res['reciepts'][i].Dist_id,'foods':foods,'date':res['reciepts'][i].Date}
    return res
            
@app.route("/getFoods")
def getFood():
    foods = FOOD_ITEM.query.all()
    for i in range(len(foods)):
        foods[i] = {"id":foods[i].Food_id,"name":foods[i].Food_name,"expiry":foods[i].Days_till_expiry}
    foods = {"food_items":foods}
    print(foods)
    return foods

@app.route("/addDon",methods=['POST'])
def addDon():
    req = request.get_json()
    last_index = DONATION.query.all()
    if last_index:
        last_index = last_index[-1].Donation_id + 1
    else:
        last_index = 1
    try:
        don = DONATION(req['date'],last_index,req['donor'],req['dist'])
        food_id = req['food_id'].split(' ')
        quantity = req['quantity'].split(' ') 
        db.session.add(don)
        db.session.commit()
        for i in range(len(food_id)):
            don_c = DONATION_CONTAINS(don.Donation_id,food_id[i],quantity[i])
            db.session.add(don_c)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        try:
            db.session.delete(don)
        except:
            pass
        db.session.commit()
        traceback.print_exc(file=sys.stdout)
        return {"status":"-1"}
    return {"status":"1"}

@app.route("/addRec",methods=['POST'])
def addRec():
    req = request.get_json()
    last_index = RECEIPT.query.all()
    if last_index:
        last_index = last_index[-1].Receipt_id + 1
    else:
        last_index = 1

    # rec = RECEIPT(last_index,req['date'],req['reciever'],req['dist'])
    try:
        rec = RECEIPT(last_index,req['date'],req['reciever'],req['dist'])
        food_id = req['food_id'].split(' ')
        quantity = req['quantity'].split(' ') 
        db.session.add(rec)
        db.session.commit()
        don = DONATION.query.filter_by(Dist_id=req['dist']).all()
        don = [x.Dist_id for x in don]

        for i in range(len(food_id)):
            food = DONATION_CONTAINS.query.filter(DONATION_CONTAINS.Donation_id.in_(don))
            food = food.filter_by(Food_id = food_id[i]).all()
            expiry = FOOD_ITEM.query.get(food_id[i]).Days_till_expiry
            amt_avail = 0
            for j in food:
                don_date = DONATION.query.get(j.Donation_id).Date
                if don_date + timedelta(days=expiry) > date(int(req['date'][:4]),int(req['date'][5:7]),int(req['date'][8:10])):
                    amt_avail += int(j.Amount)
            if amt_avail < int(quantity[i]):
                raise Exception("Insufficient food")
            rec_c = RECEIPT_CONTAINS(rec.Receipt_id,food_id[i],quantity[i])
            db.session.add(rec_c)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        try:
            db.session.delete(rec)
        except:
            pass
        db.session.commit()
        traceback.print_exc(file=sys.stdout)
        return {"status":"-1"}
    return {"status":"1"}

@app.route("/addFood", methods=['POST'])
def addFood():
    try:
        req = request.get_json()
        name = req['name']
        expiry = int(req['expiry'])
        current_foods = FOOD_ITEM.query.all()
        last_index=1
        if current_foods:
            last_index+=current_foods[-1].Food_id
        current_foods = [x.Food_name for x in current_foods]
        if name in current_foods:
            raise Exception("already exists")
        if expiry<=0:
            raise Exception("invalid expiry")
        food = FOOD_ITEM(last_index,name,expiry)
        db.session.add(food)
        db.session.commit()
    except Exception as e:
        db.session.rollback()   
        traceback.print_exc(file=sys.stdout)
        return {"status":"-1"}
    return {"status":"1"}