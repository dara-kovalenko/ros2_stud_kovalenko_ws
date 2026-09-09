from setuptools import find_packages, setup

package_name = 'stud_kovalenko_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros',
    maintainer_email='ros@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'stud_kovalenko_subscriber = stud_kovalenko_py_pkg.student_subscriber:main',
        'stud_kovalenko_monitor = stud_kovalenko_py_pkg.temperature_monitor:main',
    ],
},
)
