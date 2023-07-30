from flask import Flask
from flask_restful import Api
from api.handlers import BuyTicketResource, PostCommentResource

app = Flask(__name__)
api = Api(app)

# Adding API resources
api.add_resource(BuyTicketResource, '/buy_ticket')
api.add_resource(PostCommentResource, '/post_comment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
