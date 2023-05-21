from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QSlider, QPushButton, QSizePolicy
from PySide6.QtCharts import QtCharts
from PySide6.QtCore import Qt, QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aktienkurs")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.chart_view = QtCharts.QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chart_view)

        self.chart = QtCharts.QChart()
        self.chart.setTitle("Aktienkurs-Chart")
        self.chart.legend().hide()
        self.chart_view.setChart(self.chart)

        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setRange(0, 1)
        self.axis_x.setTickCount(5)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setRange(-100, 100)
        self.axis_y.setTickCount(5)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.series = QtCharts.QLineSeries()
        self.chart.addSeries(self.series)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.layout.addWidget(self.slider)

        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start_chart_update)
        self.layout.addWidget(self.button_start)

        self.button_stop = QPushButton("Stop")
        self.button_stop.clicked.connect(self.stop_chart_update)
        self.layout.addWidget(self.button_stop)

        self.days_label = QLabel("Anzahl der Tage: 0")
        self.layout.addWidget(self.days_label)

        self.days = 0

        self.timer = QTimer()
        self.timer.setInterval(6000)  # 6 Sekunden pro Tag
        self.timer.timeout.connect(self.update_chart)

        self.is_chart_running = False

    def slider_value_changed(self, value):
        # Aktualisiere den Einkaufspreis der Aktie
        self.chart.setTitle(f"Aktienkurs-Chart\nEinkaufspreis: {value} Euro")

    def start_chart_update(self):
        # Starte die Aktualisierung des Charts
        if not self.is_chart_running:
            self.is_chart_running = True
            self.timer.start()
            self.button_start.setEnabled(False)
            self.button_stop.setEnabled(True)

    def stop_chart_update(self):
        # Stoppe die Aktualisierung des Charts
        if self.is_chart_running:
            self.is_chart_running = False
            self.timer.stop()
            self.button_start.setEnabled(True)
            self.button_stop.setEnabled(False)

    def update_chart(self):
        # Aktualisiere den Aktienkurs für jeden Tag
        self.days += 1
        self.days_label.setText(f"Anzahl der Tage: {self.days}")

        current_price = self.slider.value()

        # Überprüfe, ob der aktuelle Preis über oder unter dem Einkaufspreis liegt
        if current_price >= 0:
            self.chart_label.setStyleSheet("QLabel { color: black; }")
        else:
            self.chart_label.setStyleSheet("QLabel { color: red; }")

        # Aktualisiere den Aktienkurs im Chart
        self.chart_label.setText(f"Aktienkurs-Chart\nEinkaufspreis: {current_price} Euro")


