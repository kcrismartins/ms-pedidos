from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, Pedido
import requests

app = Flask(__name__)
api = Api(app)

# Configuração do banco de dados RDS Aurora
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class PedidoResource(Resource):
    def get(self, pedido_id):
        pedido = Pedido.query.get(pedido_id)
        if pedido:
            return jsonify({'id': pedido.id, 'itens': pedido.itens, 'total': pedido.total, 'status': pedido.status})
        return {'message': 'Pedido não encontrado'}, 404

    def post(self):
        data = request.get_json()
        novo_pedido = Pedido(itens=data['itens'], total=data['total'], status='Pendente')
        db.session.add(novo_pedido)
        db.session.commit()
        return {'message': 'Pedido criado com sucesso', 'id': novo_pedido.id}, 201

class PagamentoResource(Resource):
    def post(self, pedido_id):
        pedido = Pedido.query.get(pedido_id)
        if pedido:
            # Simula uma chamada para o microserviço de pagamento
            pagamento_response = requests.post('http://endereco-do-microservico-de-pagamento/pagamentos', json={'pedido_id': pedido_id, 'total': pedido.total})
            if pagamento_response.status_code == 200:
                pedido.status = 'Pago'
                db.session.commit()
                return {'message': 'Pagamento realizado com sucesso'}
            else:
                return {'message': 'Falha ao realizar pagamento'}, 400
        return {'message': 'Pedido não encontrado'}, 404

api.add_resource(PedidoResource, '/pedidos', '/pedidos/<int:pedido_id>')
api.add_resource(PagamentoResource, '/pedidos/<int:pedido_id>/pagamento')

if __name__ == '__main__':
    app.run(debug=True)