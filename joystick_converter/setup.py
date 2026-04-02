from setuptools import find_packages, setup

package_name = 'joystick_converter'

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
    maintainer='fam',
    maintainer_email='fam@awadlouis.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "joystick_converter_node = joystick_converter.joystick_converter_node:main",
            "joystick_converter_consumer_node = joystick_converter.joystick_converter_consumer_node:main",
            "joy_slam_capping_node = joystick_converter.joy_slam_capping_node:main"
        ],
    },
)
