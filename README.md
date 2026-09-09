Коваленко Дар'я РТ-3


### Текстова схема системи
[Датчик LM35] ---> (Аналоговий сигнал) ---> [ESP32 АЦП (GPIO 34)] 
[ESP32] ---> (Протокол Micro XRCE-DDS через USB/Serial) ---> [micro-ROS Agent (Ubuntu)]
[micro-ROS Agent] ---> (Протокол DDS) ---> [Мережа ROS 2]
[Мережа ROS 2] ---> (Топіки /celsius та /fahrenheit) ---> [Вузол-монітор (Python)]

### Packages і firmware ESP32
*firmware ESP32* - програма написана на C++ з допомогою PlatformIO, використовуються бібліотека `micro_ros_arduino` та C-API `rclc` для таймера, реалізації вузла та двох публікаторів. Також код бере 20 замірів і потім бере середнє щоб згладити результат замірів.
*stud_kovalenko_py_pkg* - містить два файли. student_subscriber.py - підписник який допомагає зрозуміти чи все в системі працює з повідомленнями. temperature_monitor.py - файл який показує температуру в цельсіяї і фарангейтах.
*micro_ros_agent* - пакет який працює як міст між esp32 та ros2 середовищем на ubuntu.

### Таблиця класів
Ім'я класу	           | Батьківський клас	          |Поля (Атрибути)	                                                                       |  Методи
TemperatureMonitor	   | Node (з модуля rclpy.node) 	|sub_celsius (підписка на топік /celsius)sub_fahrenheit (підписка на топік /fahrenheit)  | __init__() (ініціалізація вузла та підписок)celsius_callback(msg) (обробка даних та логіка попереджень)fahrenheit_callback(msg) (вивід даних у фаренгейтах)
StudentSubscriber	     | Node (з модуля rclpy.node) 	|subscription (базова підписка для тестування)	                                         | __init__() (ініціалізація вузла)listener_callback(msg) (зчитування та логування тестових повідомлень)

### Списки nodes і topics
*Nodes*: stud_kovalenko_esp32, stud_kovalenko_monitor
*Topics*: parameter_events, rosout, stud_kovalenko/temperature/celsius, stud_kovalenko/temperature/fahrenheit

### Команди збірки та запуску
1. Збірка робочого простору - cd ~/ros2_stud_kovalenko_ws
colcon build --packages-select stud_kovalenko_py_pkg
2. Надання праав до порта - sudo chmod a+rw /dev/ttyUSB0
3. Запуск microros агента - source ~/microros_ws/install/local_setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
4. Запуск монітора - cd ~/ros2_stud_kovalenko_ws
source install/setup.bash
ros2 run stud_kovalenko_py_pkg stud_kovalenko_monitor

### Опис датчика та схема підключення
Для вимірювання температури використано аналоговий датчик LM35.
VCC: підключено до контакту 5V на платі ESP32.
GND: підключено до загальної землі (GND).
OUT: підключено до аналогового порту GPIO 34.

![Схема](scheme.jpg)

### Screenshots rqt_graph
*До підключення esp32*  ![Граф](step_7.png)
*Після підключення esp32* ![Граф](graph_with_esp32.png)

### Фізичний експеримент
| Фізичний вплив на датчик | Значення з топіка `/celsius` | Значення з топіка `/fahrenheit` | Реакція вузла-монітора (Лог у консолі) 
| Охолодження              | ~ 14.5 °C                    | ~ 58.1 °F                       | `[INFO] [stud_kovalenko_monitor]: Холодно: 14.5 °C` 
| Стан спокою              | 16.1 °C                      | 61.1 °F                         | `[INFO] [stud_kovalenko_monitor]: Норма: 16.1 °C` `[INFO] [stud_kovalenko_monitor]: Температура у Фаренгейтах: 61.1 °F` 
| Нагрівання               | 26.5 °C                      | 79.7 °F                         | `[WARN] [stud_kovalenko_monitor]: УВАГА! Температура зависока: 26.5 °C` 

### Етап 1
*Команда* colcon build: 
Starting >>> stud_kovalenko_py_pkg
Finished <<< stud_kovalenko_py_pkg [1.45s]
Summary: 1 package finished [1.60s]
*Команда* source install/setup.bash не дає якогось виводу.

*Каталог  |Опис призначення*
src	     |Директорія для зберігання коду пакетів.
build	   |Містить проміжні файли компіляції.
install	 |Зберігає файли необхідні для запуску пакетів.
log	     |Зберігає інформацію кожного процесу збірки, що допомагає при дебагінгу.

/opt/ros/jazzy/setup.bash встановлює основні системні бібліотеки необхідні для ros2, в той час як install/setup.bash лише додає локальні пакети. Без першої команди система не працювала б як слід.

### Етап 5
*Список нодів*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 node list 
/stud_kovalenko_publisher
/stud_kovalenko_subscriber
*Список топіків*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 topic list
/parameter_events
/rosout
/stud_kovalenko/message
*Які publishers і subscribers має конкретний node*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 node info /stud_kovalenko_publisher
/stud_kovalenko_publisher
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /stud_kovalenko/message: std_msgs/msg/String
  Service Servers:
    /stud_kovalenko_publisher/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /stud_kovalenko_publisher/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /stud_kovalenko_publisher/get_parameters: rcl_interfaces/srv/GetParameters
    /stud_kovalenko_publisher/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /stud_kovalenko_publisher/list_parameters: rcl_interfaces/srv/ListParameters
    /stud_kovalenko_publisher/set_parameters: rcl_interfaces/srv/SetParameters
    /stud_kovalenko_publisher/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:

  Action Clients:

*Тип повідомлення topic і хто до нього підключений*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 topic info /stud_kovalenko/message
Type: std_msgs/msg/String
Publisher count: 1
Subscription count: 1
*Структура полів типу std_msgs/msg/String*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 interface show std_msgs/msg/String
 This was originally provided as an example message.
 It is deprecated as of Foxy
 It is recommended to create your own semantically meaningful message.
 However if you would like to continue using this please use the equivalent in example_msgs.

string data
*Прочитати повідомлення з topic просто в terminal*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 topic echo /stud_kovalenko/message
data: 'Kovalenko Message #99'
---
data: 'Kovalenko Message #100'
---
data: 'Kovalenko Message #101'
---
data: 'Kovalenko Message #102'
---
data: 'Kovalenko Message #103'
---
data: 'Kovalenko Message #104'
---
data: 'Kovalenko Message #105'
---
data: 'Kovalenko Message #106'
---
data: 'Kovalenko Message #107'
---
data: 'Kovalenko Message #108'
---
data: 'Kovalenko Message #109'
---
data: 'Kovalenko Message #110'
---
data: 'Kovalenko Message #111'
---
data: 'Kovalenko Message #112'
---
data: 'Kovalenko Message #113'
---
data: 'Kovalenko Message #114'
---
data: 'Kovalenko Message #115'
---
data: 'Kovalenko Message #116'
---
data: 'Kovalenko Message #117'
---
data: 'Kovalenko Message #118'
---
data: 'Kovalenko Message #119'
---
data: 'Kovalenko Message #120'
---
data: 'Kovalenko Message #121'
---
data: 'Kovalenko Message #122'
---
data: 'Kovalenko Message #123'
---
data: 'Kovalenko Message #124'
---
data: 'Kovalenko Message #125'
---
data: 'Kovalenko Message #126'
---
^C
*Виміряти фактичну частоту публікації*
ros@ros-study:~/ros2_stud_kovalenko_ws$ ros2 topic hz /stud_kovalenko/message
WARNING: topic [/stud_kovalenko/message] does not appear to be published yet
average rate: 1.993
	min: 0.496s max: 0.510s std dev: 0.00487s window: 4
average rate: 1.999
	min: 0.491s max: 0.510s std dev: 0.00521s window: 7
average rate: 1.997
	min: 0.491s max: 0.510s std dev: 0.00510s window: 9
average rate: 2.001
	min: 0.491s max: 0.510s std dev: 0.00499s window: 12
average rate: 2.001
	min: 0.491s max: 0.510s std dev: 0.00469s window: 14
average rate: 2.000
	min: 0.491s max: 0.510s std dev: 0.00487s window: 16
average rate: 2.000
	min: 0.491s max: 0.510s std dev: 0.00462s window: 18


### Етап 6
Publisher-subscriber працює за принципом що видавець публікує повідомлення один раз в топвк який потім передає повідомлення всім підписникам одночасно. Канал зв'язку анонімний і видавець не знає скільки підписників у нього є.
Service міг би використовуватись якщо необхідно відправити конкретну команду і знати, що вона виконана.

### Етап 7
При зупинці 3 підписника він повністю зникає з графа разом зі стрілкою, що значить що повідомлення йому не йде. ![Граф](step_7.1.png)
При зупинці видавця він зникає і зникає стрілка, яка сполучала його і топік проте залишається сам топік і підписники, просто не отримують повідомлення. ![Граф](step_7.2.png)

### Етап 8

Пункт	              |Технічні характеристики датчика у проєкті
Модель	            |LM35 (у стандартних наборах найчастіше використовується модифікація LM35DZ)
Живлення	          |Напруга: від 4 В до 30 В (найчастіше підключається до піна 5V). Струм споживання: менше 60 мкА.
Інтерфейс	          |Аналоговий вихід (лінійна зміна напруги).
Діапазон	          |Від 0 °C до +100 °C (для модифікації LM35DZ) або від -55 °C до +150 °C (для базової версії LM35).
Точність	          |±0.5 °C (типова заявлена похибка при кімнатній температурі +25 °C).
Роздільна здатність	|10 мВ / 1 °C (масштабний коефіцієнт напруги).
Підключення	        |VCC датчика з'єднується з піном 5V на ESP32, GND з'єднується з піном GND, OUT з'єднується з аналоговим входом АЦП (наприклад, GPIO 34, 35 або 32).

![Фото схеми і serial monitor](photo.jpeg)

### Етап 9
1. micro-ROS Agent працює як міст між esp32 та ros2 так як мікроконтролер має замало оперативної пам'яті й є більш простим. micro-ROS Agent ніби перекладає інформацію для ros2 щоб мікроконтролер і комп'ютер спілкувались.
2. rclc вважається стабільнішою так як пам'ять на топіки і таймери виділяється лише один раз. rclcpp динамічно виділяє пам'ять, що може призвести до зависання.
3. Дані потрапляєть в DDS через кабель USB який в свою чергу зчитує дані з самого esp32.

*Команда і вивід* :
ros@ros-study:~$ ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
[1788962342.116259] info     | TermiosAgentLinux.cpp | init                     | running...             | fd: 12
[1788962342.119269] info     | Root.cpp           | set_verbose_level        | logger setup           | verbose_level: 4
[1788962351.731510] info     | Root.cpp           | create_client            | create                 | client_key: 0x1198E211, session_id: 0x81
[1788962351.731702] info     | SessionManager.hpp | establish_session        | session established    | client_key: 0x1198E211, address: 0
[1788962351.792615] info     | ProxyClient.cpp    | create_participant       | participant created    | client_key: 0x1198E211, participant_id: 0x000(1)
[1788962351.811095] info     | ProxyClient.cpp    | create_topic             | topic created          | client_key: 0x1198E211, topic_id: 0x000(2), participant_id: 0x000(1)
[1788962351.821763] info     | ProxyClient.cpp    | create_publisher         | publisher created      | client_key: 0x1198E211, publisher_id: 0x000(3), participant_id: 0x000(1)
[1788962351.834522] info     | ProxyClient.cpp    | create_datawriter        | datawriter created     | client_key: 0x1198E211, datawriter_id: 0x000(5), publisher_id: 0x000(3)
[1788962351.854644] info     | ProxyClient.cpp    | create_topic             | topic created          | client_key: 0x1198E211, topic_id: 0x001(2), participant_id: 0x000(1)
[1788962351.868359] info     | ProxyClient.cpp    | create_publisher         | publisher created      | client_key: 0x1198E211, publisher_id: 0x001(3), participant_id: 0x000(1)
[1788962351.881403] info     | ProxyClient.cpp    | create_datawriter        | datawriter created     | client_key: 0x1198E211, datawriter_id: 0x001(5), publisher_id: 0x001(3)

### Етап 12
1. Температура зростає поступово тому що пластиковому корпусу датчика потрібно пропустити крізь себе температуру перш ніж сигнал пройде до кристала всередині, який і передає сигнал.
2. Для стабілізації потрібно десь 30 секунд якщо різниця температур не є значною.
3. Охолодження проходить повільніше так як пластику важче охолоджуватись при нерухомому повітрі ніж нагріватись від теплих рук.
4. У даного датчика коливання можуть бути через те, що він аналоговий + з'єднання дротами може давати свою похибку.

Температура не може змінюватись з такою грандіозною частотою, також сам мікроконтролер просто відправлятиме безліч однакових значень, що може призвести до марної трати CPU, марної роботи DDS та роботи порту.


При виконнані даної самостійної виникли проблеми з підключенням порту, яку вдалось виправити оновленням драйвера і оголошенням його в терміналі, були проблеми з самим віртуальним середовищем - просто перезапускала проект так як він не реагував на бкдь які дії.
