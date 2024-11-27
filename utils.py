def hello():
    return "hello world"

def Athlete_histo_1(athletes, x, color, title):
  fig1 = px.histogram(athletes, x = x, color=color, title=title)
  fig1.show()