from setuptools import setup, find_packages

setup(
    name="necro-shell",
    version="1.0.0",
    description="A Haunted Terminal & Open-Source AI Engine powered by Groq LPU inference.",
    author="Hackathon Alchemist",
    py_modules=["config", "prompts", "groq_client", "cli", "web"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["static/*", "sample_code.cob", "sample_logs.txt"],
    },
    install_requires=[
        "typer>=0.9.0",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
        "flask>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "necro-shell=cli:app",
            "necro=cli:app",
        ],
    },
    python_requires=">=3.10",
)
