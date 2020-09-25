from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import math


app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["score"]=0
        session["moves"]=0
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    
    if session["turn"]=="X":
        session["moves"]=session["moves"]+1
        session["turn"]="O"
        session["board"][row][col]="X"

    else:
        session["moves"]=session["moves"]+1
        session["turn"]="X"
        session["board"][row][col]="O"

    return redirect(url_for("check"))

@app.route("/winner")

def check():

    if session["moves"]<7:

        return redirect(url_for("index"))
        

    for i in range(0,3):

        count1=0
        count2=0

        for j in range(0,3):

            if session["board"][i][j]=="X":
                count1=count1+1

            if session["board"][i][j]=="O":
                count2=count2+1

        if count1==3:
            return render_template("ok.html",player="X")

        if count2==3:
            return render_template("ok.html",player="O")

    for j in range(0,3):

        count1=0
        count2=0

        for i in range(0,3):

            if session["board"][i][j]=="X":
                count1=count1+1

            if session["board"][i][j]=="O":
                count2=count2+1

        if count1==3:
            return render_template("ok.html",player="X")

        elif count2==3:
            return render_template("ok.html",player="O")

        count1=0
        count2=0


    for i in range(0,3):

        if session["board"][i][i]=="X":
            count1=count1+1

        if session["board"][i][i]=="O":
            count2=count2+1

    if count1==3:
        session["score"]=1
        return render_template("ok.html",player="X")

    elif count2==3:
        return render_template("ok.html",player="O")

    count1=0
    count2=0

    j=0
    for i in range(2,-1,-1):

        if session["board"][j][i]=="X":
            count1=count1+1

        if session["board"][j][i]=="O":
            count2=count2+1

        j=j+1

    if count1==3:
        return render_template("ok.html",player="X")

    elif count2==3:
        return render_template("ok.html",player="O")

    count=-1

    for i in range(3):

        for j in range(3):

            if session["board"][i][j]==None:
                count=0
                count=count+1
    if count==-1:
        return render_template("tic.html",player="None")

    return redirect(url_for("index"))

@app.route("/ResetGame")

def ResetGame():
    
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]

    session["turn"] = "X"

    session["moves"]=0

    return redirect(url_for("index"))

@app.route("/computer")

def computer():

    def gameover(a):

        count=0

        for i in range(3):

            for j in range(3):

                if a[i][j]==None:
                    count=count+1

        if count==0 or check1(a)==1 or check1(a)==-1 :
            return(True)

        else:
            return(False)

    
    def check1(a):

        session["score"]=0

        for i in range(0,3):

            count1=0
            count2=0

            for j in range(0,3):

                if a[i][j]=="X":
                    count1=count1+1

                if a[i][j]=="O":
                    count2=count2+1

            if count1==3:
                session["score"]=1

            if count2==3:
                session["score"]=-1

        for j in range(0,3):

            count1=0
            count2=0

            for i in range(0,3):

                if a[i][j]=="X":
                    count1=count1+1

                if a[i][j]=="O":
                    count2=count2+1

            if count1==3:
                session["score"]=1

            elif count2==3:
                session["score"]=-1

        count1=0
        count2=0

        for i in range(0,3):

            if a[i][i]=="X":
                count1=count1+1

            if a[i][i]=="O":
                count2=count2+1

        if count1==3:
            session["score"]=1

        elif count2==3:
            session["score"]=-1

        count1=0
        count2=0

        j=0

        for i in range(2,-1,-1):

            if a[j][i]=="X":
                count1=count1+1

            if a[j][i]=="O":
                count2=count2+1

            j=j+1

        if count1==3:
            session["score"]=1

        if count2==3:
            session["score"]=-1

        return(session["score"])

    def minimax(a,b):

        if gameover(a)==True:

            return(check1(a),None,None)

        moves=[]

        for i in range(3):

            for j in range(3):

                if a[i][j]==None:

                    moves.append([i,j])
        if b=="X":

            value=-math.inf

            best=[]

            final=[]

            for move in moves:
                a[move[0]][move[1]]="X"
                x,y,z=minimax(a,"O")
                value=max(value,x)
                best.append(value)
                a[move[0]][move[1]]=None
            final=moves[best.index(max(best))]

        else:
            value=math.inf

            best=[]

            final=[]

            for move in moves:
                a[move[0]][move[1]]="O"
                x,y,z=minimax(a,"X")
                value=min(value,x)
                best.append(value)
                a[move[0]][move[1]]=None

            final=moves[best.index(min(best))]

        return(value,final[0],final[1])

    value,row,col=minimax(session["board"],session["turn"])

    return redirect(url_for("play",row=row,col=col))