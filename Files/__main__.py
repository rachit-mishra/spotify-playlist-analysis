import sys
from features_processing import * 
import features_processing as f

def main():
    """ This is the main routine """
    f.main(username, playlist)
    

if __name__ == "__main__":
    sc = SparkContext()
    sc.setLogLevel("WARN")
    sqlContext = HiveContext(sc)
    username = sys.argv[1]
    playlist = sys.argv[2]
    main()
