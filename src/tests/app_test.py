import unittest
from app import app, warehouses, warehouse_counter


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        warehouses.clear()
        warehouse_counter[0] = 0

    def test_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_shows_no_warehouses_message(self):
        response = self.client.get('/')
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_warehouse_get_returns_200(self):
        response = self.client.get('/warehouse/new')
        self.assertEqual(response.status_code, 200)

    def test_create_warehouse_post_creates_warehouse(self):
        response = self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouses), 1)

    def test_view_warehouse_returns_200(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        response = self.client.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)

    def test_view_nonexistent_warehouse_redirects(self):
        response = self.client.get('/warehouse/999')
        self.assertEqual(response.status_code, 302)

    def test_add_to_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        self.client.post('/warehouse/1/add', data={'amount': '25'})
        self.assertAlmostEqual(warehouses[1]['varasto'].saldo, 25)

    def test_remove_from_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '50'
        })
        self.client.post('/warehouse/1/remove', data={'amount': '25'})
        self.assertAlmostEqual(warehouses[1]['varasto'].saldo, 25)

    def test_edit_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Original',
            'capacity': '100',
            'initial': '0'
        })
        self.client.post('/warehouse/1/edit', data={'name': 'Renamed'})
        self.assertEqual(warehouses[1]['name'], 'Renamed')

    def test_delete_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        self.assertEqual(len(warehouses), 1)
        self.client.post('/warehouse/1/delete')
        self.assertEqual(len(warehouses), 0)
