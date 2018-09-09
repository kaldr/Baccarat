# import Learn.App
# import GUI.App

from Baccarat.Game import Play

# import CV.BasicCV
play = Play(playTime=40, roundLimit=100,
            params={"output_path": '/Users/kaldr/Projects/Baccarat/Export/drop_with_round/',
                    'play_type': "drop_with_round", 'stopWhenProfitMoney': 4000})
for i in range(40):
    play.play_baccarat(i)
# import GUI.Mouse

# from Baccarat.Baccarat import Baccarat
# from Poker.Card import Card

# # b=Baccarat()
# # print(b.cards)
# c = Card()
# print(c.decks_of_cards(2))
#

# import random

# l = [1, 2, 5]
# time = 20
# total = 0
# for i in range(time):
#     score = random.randrange(3)
#     total += l[score]
# print(total)
# print("%.2f" % (total / time))
#
# import pyscreenshot
# import flask
# from io import BytesIO

# app = flask.Flask(__name__)

# @app.route('/screen.png')
# def serve_pil_image():
#     img_io = BytesIO()
#     pyscreenshot.grab().save(img_io, 'PNG', quality=50)
#     img_io.seek(0)
#     return flask.send_file(img_io, mimetype='image/png')

# @app.route('/')
# def serve_img():
#     return flask.render_template('screen.html')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)
