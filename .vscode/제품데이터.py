import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
import sqlite3

# DB 함수 (제품데이터.py와 동일)
conn = sqlite3.connect('products.db')
cur = conn.cursor()

def insert_product(productid, productname, productprice):
    try:
        cur.execute('INSERT INTO products (productid, productname, productprice) VALUES (?, ?, ?)',
                    (productid, productname, productprice))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def update_product(productid, productname=None, productprice=None):
    if productname is not None:
        cur.execute('UPDATE products SET productname=? WHERE productid=?', (productname, productid))
    if productprice is not None:
        cur.execute('UPDATE products SET productprice=? WHERE productid=?', (productprice, productid))
    conn.commit()

def delete_product(productid):
    cur.execute('DELETE FROM products WHERE productid=?', (productid,))
    conn.commit()

def select_products():
    cur.execute('SELECT * FROM products')
    return cur.fetchall()

# PyQt5 UI
class ProductApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제품 관리')
        self.setGeometry(100, 100, 500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 입력 폼
        form_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('제품ID')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('제품명')
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText('가격')
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.price_input)
        self.layout.addLayout(form_layout)
        
        
        # 버튼
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton('입력')
        self.update_btn = QPushButton('수정')
        self.delete_btn = QPushButton('삭제')
        self.search_btn = QPushButton('검색')
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.search_btn)
        self.layout.addLayout(btn_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['제품ID', '제품명', '가격'])
        self.layout.addWidget(self.table)

        # 이벤트 연결
        self.add_btn.clicked.connect(self.add_product)
        self.update_btn.clicked.connect(self.update_product)
        self.delete_btn.clicked.connect(self.delete_product)
        self.search_btn.clicked.connect(self.load_products)
        self.table.cellClicked.connect(self.table_clicked)

        self.load_products()

    def add_product(self):
        try:
            pid = int(self.id_input.text())
            name = self.name_input.text()
            price = int(self.price_input.text())
            if not name:
                raise ValueError
            if insert_product(pid, name, price):
                QMessageBox.information(self, '성공', '제품이 추가되었습니다.')
            else:
                QMessageBox.warning(self, '오류', '이미 존재하는 제품ID입니다.')
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '모든 값을 올바르게 입력하세요.')

    def update_product(self):
        try:
            pid = int(self.id_input.text())
            name = self.name_input.text()
            price = self.price_input.text()
            if not name and not price:
                QMessageBox.warning(self, '입력 오류', '수정할 값을 입력하세요.')
                return
            update_product(pid, name if name else None, int(price) if price else None)
            QMessageBox.information(self, '성공', '제품이 수정되었습니다.')
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '제품ID와 가격은 숫자여야 합니다.')

    def delete_product(self):
        try:
            pid = int(self.id_input.text())
            delete_product(pid)
            QMessageBox.information(self, '성공', '제품이 삭제되었습니다.')
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '제품ID를 올바르게 입력하세요.')

    def load_products(self):
        self.table.setRowCount(0)
        for row_data in select_products():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, data in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def table_clicked(self, row, col):
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec_())