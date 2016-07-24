import csv

movies = []
def convert2csv():
    with open('movies.txt','r') as infile:
        movies = infile.readlines()

    infile.close()
    with open('movies.csv','w') as out:
        out.write('productId,userId,profileName,helpfulness,score,time,summary,text\n')
        count=0
        output=''
        for row in movies:
            if row.rstrip()!='':
                count+=1
                if count%8!=0:
                    read = row.split(':')
                    read[1] = read[1].replace(',','')
                    read[1] = read[1].replace('\n','')
                    read[1] = read[1].replace('<br />','')
                    read[1] = read[1].replace('\\','')
                    output += str(read[1])+','
                if count%8==0:
                    read = row[row.find(':')+1:]
                    read = read.replace(',','')
                    read = read.replace('\n','')
                    read = read.replace('<br />','')
                    read = read.replace('\\','')
                    output += str(read)+','
                    out.write(output)
                    output='\n'
    return            
    
def helpscore():
    calcScore = {}
    with open('helpful-score.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        header = reader.next()
    
        for row in reader:
            value = row[1].split('/')
            if value[1] =='0':
                score = 0
            else:
                score = float(value[0])/float(value[1])
            calcScore[row[0]] = score * 250
    infile.close()
    
    with open('helpful-scores.csv','w') as out:
        out.write('Count,ProductID,Score\n')
        count = 1
        for data in calcScore:
            out.write(str(count) + ',' + data + ',' + str(calcScore.get(data)) + '\n')
            count +=1
    out.close()
    return

def convert2json():
    comments = []
    with open('comment-count.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        header = reader.next()

        for row in reader:
            comments.append(row[0]+'/'+row[1])
    infile.close()
    with open('comments.json','w') as out:
        json = '{\n"name" : "Number of reviews",\n'
        json+= '"parent" : "null", \n"children" : ['
        with open('movie-comments.csv','r') as infile:
            reader = csv.reader(infile.read().splitlines())
            header = reader.next()
            num = len(comments)
            print num
            i = 0
            count = 0
            temp = 0
            for row in reader:
                if count == 0 and i<num:
                    value = comments[i].split('/')                    
                    count = int(value[1])
                    if count>50:
                        temp = 50
                    else:
                        temp = count
                    if i!= 0:
                        json += ']},\n{\n'
                    else:
                        json += '{\n'
                    json += '"name" : "' + value[0] + '",\n'
                    json += '"parent" : "Number of reviews",\n'
                    json += '"children" : [\n'
                    count = count - 1
                    temp = temp - 1
                    json += '{"name" : "' + row[0].rstrip() + '",\n'
                    json += '"parent" : "' + row[1].rstrip() + '"}'
                    if temp!=0:
                        json+=',\n'
                    else:
                        json += '\n'
                    print i
                    i+=1
                elif temp>0:
                    count = count - 1
                    temp = temp - 1
                    json += '{"name" : "' + row[0].rstrip() + '",\n'
                    json += '"parent" : "' + row[1].rstrip() + '"}'
                    #print str(i) + " " + str(temp)
                    if temp!=0:
                        json+=',\n'
                    else:
                        json += '\n'
                elif i<num and count>0:
                    count = count-1
                    continue
            json += ']}]}'
        infile.close()
        out.write(json)
    out.close()
                    
    return

#helpscore()
convert2json()
