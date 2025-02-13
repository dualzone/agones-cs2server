from setuptools import setup, find_packages
setup(
    name='Agones dualzone CS2 manager',  # Choisis un nom pour ton package
    version='0.1',
    packages=find_packages(),
    install_requires=[  # Liste des dépendances
        # Exemple : 'requests>=2.25.0'
    ],
    include_package_data=True,  # Assure que les fichiers non-Python sont inclus
    entry_points={  # Points d'entrée pour ton application, si nécessaire
        'console_scripts': [
            'mon_script=main:main',  # Remplace 'main' avec la fonction de démarrage
        ],
    },
)