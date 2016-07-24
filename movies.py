import csv
import datetime as dt

products = {}

def uniqueProducts():
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            pid = row[0].rstrip()
            if products.has_key(pid):
                products[pid]=products.get(pid) + 1
            else:
                products[pid] = 1
    movie.close()
    with open('output/movie-comments.csv','w') as out:
        out.write('ProductID,Count\n')
        for data in products:
            out.write(data + ',' + str(products.get(data)) + '\n')
    out.close()
    return

month = {}
years = {}
day = {}
month_year = {}
def findTime():
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            pid = row[0].rstrip()
            time = row[5].rstrip()
            year = dt.datetime.fromtimestamp(int(time)).strftime('%Y')
            months = dt.datetime.fromtimestamp(int(time)).strftime('%m')
            date1 = dt.datetime.fromtimestamp(int(time)).strftime('%d')
            date_obj = dt.date(int(year),int(months),int(date1))
            days = dt.date.isoweekday(date_obj)
            if month_year.has_key(months+'/'+year):
                month_year[months+'/'+year]=month_year.get(months+'/'+year) + 1
            else:
                month_year[months+'/'+year] = 1
            if month.has_key(months):
                month[months]=month.get(months) + 1
            else:
                month[months] = 1
            if day.has_key(days):
                day[days]=day.get(days) + 1
            else:
                day[days] = 1
            if years.has_key(year):
                years[year]=years.get(year) + 1
            else:
                years[year] = 1
    movie.close()
    with open('output/review-days.csv','w') as out:
        out.write('Day,Count\n')
        for data in day:
            day_name = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            out.write(day_name[data-1] + ',' + str(day.get(data)) + '\n')
    out.close()
    with open('output/review-year.csv','w') as out:
        out.write('Year,Count\n')
        for data in years:
            out.write(data + ',' + str(years.get(data)) + '\n')
    out.close()
    with open('output/review-month.csv','w') as out:
        out.write('Month,Count\n')
        month_name = ['January','February','March','April','May','June','July','August','September','October','November','December']
        for data in month:
            out.write(month_name[int(data)-1] + ',' + str(month.get(data)) + '\n')
    out.close()
    with open('output/month_year.csv','w') as out:
        out.write('Month,Count\n')
        for data in month_year:
            out.write(data + ',' + str(month_year.get(data)) + '\n')
    out.close()
    return

reviewers = {}

def uniqueReviewers():
    num = {}
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            user = row[2].rstrip()
            if reviewers.has_key(user):
                reviewers[user]=reviewers.get(user) + 1
            else:
                reviewers[user] = 1
    movie.close()
    #print len(reviewers)
    with open('output/users.csv','w') as out:
        out.write('Name,Count\n')
        for data in reviewers:
            out.write(data + ',' + str(reviewers.get(data)) + '\n')
            value = str(reviewers.get(data))
            if num.has_key(value):
                num[value] = num.get(value)+1
            else:
                num[value] = 1
    out.close()
    with open('output/user-count.csv','w') as out:
        out.write('user-count,Count\n')
        for data in num:
            out.write(data + "," + str(num.get(data))+'\n')
    return

helps = {}
def helpfulness():
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            pid = row[0].rstrip()
            score = row[3].rstrip()
            value = score.split('/')
            num=value[0]
            den=value[1]
            if den == '0':
                den = '1'
            key = float(num)/float(den)
            if helps.has_key(pid):
                helps[pid] = helps.get(pid) + key
            else:
                helps[pid] = key
    movie.close()
    #print len(helps)
    with open('output/helpful-score.csv','w') as out:
        out.write('ProductID,Score\n')
        for data in helps:
            out.write(str(data) + "," + str(helps.get(data))+'\n')
    out.close()
    return

scores = {}
def calculateScore():
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            pid = row[0].rstrip()
            rate = row[4].rstrip()
            if scores.has_key(pid):
                scores[pid] = scores.get(pid) + float(rate)
            else:
                scores[pid] = float(rate)
    movie.close()
    with open('output/movie-scores.csv','w') as out:
        out.write('ProductID,Score\n')
        for data in scores:
            out.write(data + ',' + str(scores.get(data)) + '\n')
    out.close()
    return

def topmovies():
    mov_com = {}
    with open('output/movie-comments.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        reader.next()
        for row in reader:
                mov_com[row[0].rstrip()] = row[1].rstrip()
    infile.close()
    #print len(mov_com)
    with open('output/helpful-score.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        reader.next()
        with open('output/countscore.csv','w') as out:
            out.write('ProductID,Count,Score\n')
        out.close()
        for row in reader:
            if mov_com.has_key(row[0].rstrip()):
                with open('output/countscore.csv','a') as out:
                    out.write(row[0].rstrip() + ',' + mov_com.get(row[0].rstrip()) + ','+ row[1].rstrip() + '\n')
                out.close()
    infile.close()
    return

def summaryNLP():
    words = {}
    afinn = []
    summary = {}
    count_sum = {}
    with open('AFINN-111.txt','r') as infile:
        afinn = infile.readlines()
    infile.close()
    for data in afinn:
        row = data.split('\t')
        words[row[0]] = row[1]
    with open('movies.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        reader.next()
        for row in reader:
            text = row[6].rstrip().split()
            summ = 0
            count_summary = 0
            for data in text:
                if words.has_key(data):
                    summ+= int(words.get(data))
                    if words.get(data)!='0':
                        count_summary += 1

            if summary.has_key(row[0].rstrip()):
                summary[row[0].rstrip()] = summary.get(row[0].rstrip()) + float(summ)/float(count_sum.get(row[0].rstrip()))
            else:
                if count_summary!=0:
                    count_sum[row[0].rstrip()] = float(count_summary)
                    summary[row[0].rstrip()] = float(summ)/float(count_sum.get(row[0].rstrip()))
                else:
                    count_sum[row[0].rstrip()] = 1
                    summary[row[0].rstrip()] = 0
    infile.close()
    #print len(summary)
    with open('output/summary-score.csv','w') as out:
        out.write('ProductID,Summary Score,Movie Score\n')
        for data in summary:
            out.write(str(data) + "," + str(summary.get(data)/products.get(data))+"," + str(scores.get(data)/products.get(data))+'\n')
    out.close()
    return

def reviewNLP():
    words = {}
    afinn = []
    summary = {}
    count_sum = {}
    with open('AFINN-111.txt','r') as infile:
        afinn = infile.readlines()
    infile.close()
    for data in afinn:
        row = data.split('\t')
        words[row[0]] = row[1]
    with open('movies.csv','r') as infile:
        reader = csv.reader(infile.read().splitlines())
        reader.next()
        for row in reader:
            text = row[7].rstrip().split()
            summ = 0
            count_summary = 0
            for data in text:
                if words.has_key(data):
                    summ+= int(words.get(data))
                    if words.get(data)!='0':
                        count_summary += 1
            
            if summary.has_key(row[0].rstrip()):
                summary[row[0].rstrip()] = summary.get(row[0].rstrip()) + float(summ)/float(count_sum.get(row[0].rstrip()))
            else:
                if count_summary!=0:
                    count_sum[row[0].rstrip()] = float(count_summary)
                    summary[row[0].rstrip()] = float(summ)/float(count_sum.get(row[0].rstrip()))
                else:
                    count_sum[row[0].rstrip()] = 1
                    summary[row[0].rstrip()] = 0
    infile.close()
    #print len(summary)
    with open('output/Review-score.csv','w') as out:
        out.write('ProductID,Review Score,Movie Score\n')
        for data in summary:
            out.write(str(data) + "," + str(summary.get(data)/products.get(data))+"," + str(scores.get(data)/products.get(data))+'\n')
    out.close()
    return

uniqueProducts()
calculateScore()
reviewNLP()
summaryNLP()
topmovies()
findTime()
uniqueReviewers()
helpfulness()

