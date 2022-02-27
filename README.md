# carlos_gnss

Prequisites:

- Running instance of Carla Simulator [Version 0.9.12] (https://github.com/carla-simulator/)
- Carla [Version 0.9.12] Python module installed -- `pip3 install carla`
- Python version 3.8 (not tested on other versions)

For reference how the program works, you can take a look into the `example.py` file. Simply import the module `api` and instantiate `Api` with the host adress (where the Carla instance is running), port address, relevance radius (in what range other vehicle should be detected) and max entry count (amout of each datatype to save for each actor into CSV file).
After instantiating, run the `start` method of the instance with the argument how often the position data should be polled (in s).

Since the program runs in a seperate thread, the code will immediately continue to run after `start` which is why there is an `input` that keeps the code running.
After finishing the run you can save the data into a file by defining the path and dataname.

Here's a short example:
```
from api import Api
if __name__ == "__main__":
    a: Api = Api('localhost', 2000, 50000, 10)
    a.start(0.5)
    input("Press ENTER to end")
    a.save_csv(r"\path\to\folder", "filename.csv")
    a.stop()

```

For more information feel free to look into the code and read the docstrings.
