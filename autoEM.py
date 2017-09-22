#!/usr/bin/python
import os
import re

def run():
#    filename="caracu"
#    (parameters,data,sortnum)=findQuadPlots(".")
#    filters="#nada"
#    save_results(data,filename,filters,parameters,sortnum)
    gotdata=readDefocusFile(".","FoilHole_6484231_Data_6477137_6477138_20140308_205759")
    print gotdata
class autoEM:
    def helloMan(self):
        message="Hello Man"
        return message

    def findQuadPlots(self,directory,logdir="log",pngdir="ctf"):
        """ Finds pngs and then finds the corresponding log file 
        """
        my_params=["Micrograph_Identity","Ignore","DF1","DF2","Angast","CCC","Defocus","CC","apix","kV","Mag"]
        my_parlist=[]
        for pngs in os.listdir(directory+"/"+pngdir):
            li=[]
            li.append(pngs[:-4])
            li.append(1)
            if os.path.isfile(directory+"/"+li[0]+".defocus"):
                pars=readDefocusFile(directory,li[0])
            elif os.path.isfile(directory+"/"+logdir+"/"+li[0]+".log"):
                pars=readLogfiles(directory,li[0])
            else:
                pars=0
            if pars:
                li.extend(pars)
                #print li
                my_parlist.append(li)
        qloc=1
        #print my_params
        return my_params,my_parlist,qloc

    def readDefocusFile(self,mydirectory,myfile):
        """Read parameters from the .defocus file
        """
        mydata=[]
        try:
            f=open(mydirectory+"/"+myfile+".defocus")
            for i in f.readline().rstrip('\n').split(" \t ")[1:8]:
                mydata.append(float(i))
            return mydata [:1]+mydata[4:7]+mydata[1:3]+[-1,-1,-1]


        except IOError, AttributeError:
            return



    def readLogfiles(self,mydirectory,myfile,logdir="log"):
        """Finds the CTF line in the log file
        """
        mypattern=re.compile(r"CTF parameters = \[(\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+), (\d+.\d+)\]")
        mydata=[]
        try:
            mylog=open(mydirectory+"/"+logdir+"/"+myfile+".log")
            for line in mylog:
                myfinding=mypattern.match(line)
                if myfinding:
                    mylog.close()
                    for i in myfinding.groups():
                        mydata.append(float(i))

                    return mydata


        except IOError, AttributeError:
            return



    def get_parameters(self):
        if os.path.isfile(self.dbin):
            parameter_file=open(self.dbin,"r")
            self.read_dbase(parameter_file)
            return self.parameters,self.rawlist,self.qloc
        else:
            print "File "+ self.dbin +" not found, reading log files"
            return findQuadPlots(".")


    def read_dbase(self,f):
        self.parameters=[]
        self.rawlist=[]
        sortnum=-1

        while True:
            line=f.readline()
            if line[0]=="*":
                line=line[1:].split()
                #print line
                if line[0]=="Filter:":
                    for n in range(1,len(line)):
                        sp=line[n].split("|")
                        try:
                            temp=float(sp[3])
                            filters.append([sp[0],sp[1],sp[2],str(temp)])
                        except ValueError:
                            tkMessageBox.showerror("Error", "Invalid integer in input file")
                if line[0]=="Sort:":
                    sortnum=int(line[1])
                continue
            line=line.split("\t")
            for i, param in enumerate(line):
                self.parameters.append(param)
                self.parameters[-1]=self.parameters[-1].strip("\n")
            break
    # Location of quality/ignore in self.parameters
        self.qloc = -1
        if not "Ignore" in self.parameters:
            self.parameters.append("Ignore")
        else:
            self.qloc=self.parameters.index("Ignore")
     # Process list
        while True:
            line=f.readline()
            if not line:
                break


            line=line.split("\t")
            for i in range(len(self.parameters)):
                try:
                    line[i]=float(line[i])
                except ValueError:
                    pass
                except IndexError:
                    if self.qloc<0:
                        line.append("-")
            line.append(1)

            self.rawlist.append(line)
        f.close()

#        return self.parameters,self.rawlist,self.qloc

    def save_results(self,sortnum):
        f=open(self.dbout,mode='w')
        # Write Header
        l = "* Filters used:"
        for fil in self.filters:
            l+=" "+(" ").join(fil)
            l+=","
        if len(self.filters)==0:
            l+=" none"
        else:
            l=l[:-1]
        f.write(l+"\n")
        if not sortnum==-1:
            f.write("* Sorted by: "+self.parameters[sortnum]+"\n")
        # Write parameters
        for param in self.parameters:
            f.write(param+"\t")
        f.write("\n")
        # Write data
        for datapoint in self.imagelist:
                [f.write("{0}\t".format(datapoint[x])) for x in range(0,len(self.parameters)-1)]
                f.write("{0}\n".format(datapoint[len(self.parameters)-1]))
        f.close()

    def save_list_file(self,outfile):
        f=open(outfile,mode='w')
        for datapoint in self.imagelist:
            f.write("{0}\n".format(datapoint[0]))
        f.close()

    def sortby(self,parameter,descending):
        self.sortnum=self.parameters.index(parameter)
        current_entry=self.imagelist[self.counter][0]
        self.imagelist.sort(key=lambda tup:tup[self.sortnum],reverse=descending)
        self.counter=self.get_index(self.imagelist,current_entry)
        #self.dbo.counter=self.dbo.imagelist.index(current_name)


    def get_index(self,data,query):
        count=-1
        for record in data:
            count+=1
            if query==record[0]:
                break
        return count

    def dofilter(self):
        for i in self.rawlist:
            i[-1]=1
        for f in self.filters:
            if f[0]=="Remove":
                self.rem_show(f,-1)
            elif f[0]=="Show":
                self.rem_show(f,1)

    def rem_show(self,f,num):
        d=0
        if num>0:
            d=1
        n=self.parameters.index(f[1])
        for i in self.rawlist:
            if ((f[2]==">" and i[n]>float(f[3]))
                or (f[2]==">=" and i[n]>=float(f[3]))
                or (f[2]=="=" and i[n]==float(f[3]))
                or (f[2]=="<=" and i[n]<=float(f[3]))
                or (f[2]=="<" and i[n]<float(f[3]))):
                i[-1]=d


    def __init__(self, name=None, parameters=None):
#        UserDict.__init__(self)
        print name
        self.dbin = name
        self.dbout= ""
        self.parameters=[]
        self.rawlist=[]
        self.imagelist=[]
        self.filters=[]
        self.sortnum=-1
        self.counter=0
        self.sortorder=0
        if parameters:
            self.parameters.extend(parameters)
        else:
            self.parameters=["Micrograph_Identity","Ignore","DF1","DF2","Angast","CCC","Defocus","CC","apix","kV","Mag"]
 
class microGraph:
    def read_boxfile(self,boxfile=None,boxdir=None):
        """Read the .box file
        """
        if not boxfile:
            boxfile=self.name+".box"
        if not boxdir:
            boxdir=self.boxdir
        try:
            f=open(boxdir+"/"+boxfile)

            for line in f:
                cnt=0
                mydata=[]
                for i in line.rstrip('\n').split(' '):
                    cnt=cnt+1
                    mydata.append(float(i))
                self.boxes.append(mydata)
            f.close

        except IOError, AttributeError:
            print "Error opening %s/%s..." % (boxdir,boxfile)
            return
    def write_boxfile(self,boxdir,boxfile):
        """write the .box file
        """
        if not boxfile:
            boxfile=self.name+".box"
        if not boxdir:
            boxdir=self.boxdir
        try:
            f=open(boxdir+"/"+boxfile,'w')
            for box in self.boxes:
                f.write("%d\t%d\t%d\t%d\n" % (box[0],box[1],box[2],box[3]))
            f.close

        except IOError, AttributeError:
            print "Error opening %s/%s..." % (boxdir,boxfile)
            return
    def bin_boxes(self,binning):
        for box in self.boxes:
            box[0]=box[0]/binning
            box[1]=box[1]/binning
    def __init__(self, name=None, parameters=None, boxdir=None):
        print name
        self.boxes=[]
        self.name=name
        self.boxdir=boxdir


if __name__ == '__main__':
    run()
