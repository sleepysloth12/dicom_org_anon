from setuptools import setup, find_packages

setup(
    name='dicom_org_anon',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dicom_org_anon=main:main'  # Adjust if your main function is named differently
        ]
    },
    install_requires=[
        # List your project dependencies here
        'pydicom',
        'tkinter',
          'csv', 'json', 'os','shutil','random' 
    ],
)
