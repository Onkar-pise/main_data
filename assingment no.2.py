with open('demo_assingment.txt','r+') as fp:
    data=fp.read()
    fp.write('\n#### this new content:')
    fp.seek(0)
    fp.write('this old output :\n')
    d=fp.read()

