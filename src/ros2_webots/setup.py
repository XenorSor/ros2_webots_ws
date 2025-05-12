import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ros2_webots'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share' + package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.wbt')),
        (os.path.join('share', package_name, 'resource'), glob('resource/*.urdf'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='xenor',
    maintainer_email='xenor@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #'car_driver = ros2_webots.car_driver:main'
        ],
    },
)
