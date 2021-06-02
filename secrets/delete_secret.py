#!/usr/bin/env python3
from paspymod.funct_tools import query_request, other_requests
from paspymod.logger import logging as log
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get secret info.")
    parser.add_argument('-n','--Name', type=str, required=True, help= 'Name of Secret')
    args = parser.parse_args()