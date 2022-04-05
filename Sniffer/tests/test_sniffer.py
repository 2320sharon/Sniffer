import pytest
import os
from Sniffer import sniffer


def test_change_filename():
   # Make an instance of the Sniffer Class   
    sniffer_app = sniffer.SnifferClass()
    sorted_dir=os.getcwd()+os.sep+"test_dir"
    old_filename="old_filename.jpg"
    sort_type="good"
    new_filename_loc=sniffer_app.change_filename(old_filename,sort_type,sorted_dir)
    assert new_filename_loc == sorted_dir+os.sep+"old_filename_good.jpg"
