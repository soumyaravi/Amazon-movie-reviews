import csv
import os
import datetime as dt
words = {}

def create_initial():
    afinn = []
    with open('AFINN-111.txt', 'r') as infile:
        afinn = infile.readlines()
    infile.close()
    for data in afinn:
        row = data.split('\t')
        words[row[0]] = row[1]
    return

avg_rating = {}

def top_rated_movies():
    totalscores = {}

    # read total scores
    with open('output/movie-scores.csv', 'r') as infile:
        reader = csv.reader(infile)
        reader.next()

        for row in reader:
            totalscores[row[0]] = row[1]
    infile.close()
    #print len(totalscores)
    products = {}
    # read unique products
    with open('output/movie-comments.csv', 'r') as infile:
        reader = csv.reader(infile)
        reader.next()

        for row in reader:
            products[row[0]] = row[1]
    infile.close()
    #print len(products)
    scores = {}
    summary = {}
    for data in totalscores:
        val = float(totalscores.get(data)) / float(products.get(data))
        scores[data] = val
    with open('output/summary-score.csv', 'r') as infile:
        reader = csv.reader(infile)
        reader.next()

        for row in reader:
            summary[row[0]] = float(row[1])
            avg_rating[row[0]] = float(row[2])
    infile.close()
    ten = int(0.1 * len(scores))
    twenty = int(0.2 * len(scores))
    bottom = int(0.5 * len(scores)) + 1
    comm10 = {'positive': 0, 'negative': 0, 'neutral': 0}
    comm20 = {'positive': 0, 'negative': 0, 'neutral': 0}
    comm30 = {'positive': 0, 'negative': 0, 'neutral': 0}
    comm50 = {'positive': 0, 'negative': 0, 'neutral': 0}
    comments = {'10': 0, '11-30': 0, '31-50': 0, '51': 0}
    count = 0
    for data in sorted(scores, key=scores.get, reverse=True):
        val = summary.get(data)
        if count <= ten:
            comments['10'] = comments.get('10') + int(products.get(data))
            if val > 0:
                comm10['positive'] = comm10.get('positive') + 1
            elif val < 0:
                comm10['negative'] = comm10.get('negative') + 1
            else:
                comm10['neutral'] = comm10.get('neutral') + 1
        elif count > ten and count <= twenty:
            comments['11-30'] = comments.get('11-30') + int(products.get(data))
            if val > 0:
                comm20['positive'] = comm20.get('positive') + 1
            elif val < 0:
                comm20['negative'] = comm20.get('negative') + 1
            else:
                comm20['neutral'] = comm20.get('neutral') + 1
        elif count > twenty and count < bottom:
            comments['31-50'] = comments.get('31-50') + int(products.get(data))
            if val > 0:
                comm30['positive'] = comm30.get('positive') + 1
            elif val < 0:
                comm30['negative'] = comm30.get('negative') + 1
            else:
                comm30['neutral'] = comm30.get('neutral') + 1
        else:
            comments['51'] = comments.get('51') + int(products.get(data))
            if val > 0:
                comm50['positive'] = comm50.get('positive') + 1
            elif val < 0:
                comm50['negative'] = comm50.get('negative') + 1
            else:
                comm50['neutral'] = comm50.get('neutral') + 1
        count += 1
    if os.path.isfile('output/Comments.tsv'):
        os.remove('output/Comments.tsv')
    with open('output/Comments.tsv', 'a') as out:
        out.write('Category\tCount\n')
        for data in comments:
            out.write(data + '\t' + str(comments.get(data)) + '\n')
    out.close()
    if os.path.isfile('output/top10.tsv'):
        os.remove('output/top10.tsv')
    with open('output/top10.tsv', 'a') as out:
        out.write('Category\tCount\n')
        for data in comm10:
            out.write(data + '\t' + str(comm10.get(data)) + '\n')
    out.close()
    if os.path.isfile('output/top11-30.tsv'):
        os.remove('output/top11-30.tsv')
    with open('output/top11-30.tsv', 'a') as out:
        out.write('Category\tCount\n')
        for data in comm20:
            out.write(data + '\t' + str(comm20.get(data)) + '\n')
    out.close()
    if os.path.isfile('output/top31-50.tsv'):
        os.remove('output/top31-50.tsv')
    with open('output/top31-50.tsv', 'a') as out:
        out.write('Category\tCount\n')
        for data in comm10:
            out.write(data + '\t' + str(comm30.get(data)) + '\n')
    out.close()
    if os.path.isfile('output/bottom50.tsv'):
        os.remove('output/bottom50.tsv')
    with open('output/bottom50.tsv', 'a') as out:
        out.write('Category\tCount\n')
        for data in comm10:
            out.write(data + '\t' + str(comm50.get(data)) + '\n')
    out.close()
    return


def review_sentiment():
    users = {}
    with open('output/users.csv', 'r') as infile:
        reader = csv.reader(infile)
        reader.next()

        for row in reader:
            users[row[0].rstrip()] = int(row[1])
    infile.close()

    first = {'positive': 0, 'negative': 0, 'neutral': 0}
    frequent = {'positive': 0, 'negative': 0, 'neutral': 0}
    positive = {'first': 0, 'frequent': 0}
    negative = {'first': 0, 'frequent': 0}
    neutral = {'first': 0, 'frequent': 0}
    ratings_new = {'yes':0,'no':0}
    ratings_frequent = {'yes':0,'no':0}
    pf1, pf2, nf1, nf2, ne1, ne2 = 0, 0, 0, 0, 0, 0
    with open('movies.csv', 'r') as infile:
        reader = csv.reader(infile)
        reader.next()
        # print header
        for row in reader:
            user = row[2].rstrip()
            text = row[6].rstrip().split()
            rating = float(row[4].rstrip())
            summ = 0
            count = 0
            for data in text:
                if words.has_key(data) and words.get(data) != 0:
                    summ += int(words.get(data))
                    count += 1
            if count == 0:
                count = 1
            val = float(summ) / float(count)
            if (users.get(user)) == 1:
                if val > 0:
                    first['positive'] = first.get('positive') + 1
                    pf1 += 1
                    positive['first'] = float(positive.get('first') + rating)
                elif val < 0:
                    first['negative'] = first.get('negative') + 1
                    nf1 += 1
                    negative['first'] = float(negative.get('first') + rating)
                else:
                    first['neutral'] = first.get('neutral') + 1
                    ne1 += 1
                    neutral['first'] = float(neutral.get('first') + rating)
                try:
                    if abs(rating-avg_rating.get(row[0].rstrip()))<0.5:
                        ratings_new['yes'] = ratings_new.get('yes') + 1
                    else:
                        ratings_new['no'] = ratings_new.get('no') + 1
                except TypeError:
                    pass
            elif (users.get(user)) > 9:
                if val > 0:
                    frequent['positive'] = frequent.get('positive') + 1
                    pf2 += 1
                    positive['frequent'] = float(positive.get('frequent') + rating)
                elif val < 0:
                    frequent['negative'] = frequent.get('negative') + 1
                    nf2 += 1
                    negative['frequent'] = float(negative.get('frequent') + rating)
                else:
                    frequent['neutral'] = frequent.get('neutral') + 1
                    ne2 += 1
                    neutral['frequent'] = float(neutral.get('frequent') + rating)
                try:
                    if abs(rating - avg_rating.get(row[0].rstrip()))<0.25:
                        ratings_frequent['yes'] = ratings_frequent.get('yes') + 1
                    else:
                        ratings_frequent['no'] = ratings_frequent.get('no') + 1
                except TypeError:
                    pass
            else:
                continue

        with open('output/New Reviewers.tsv', 'w') as out:
            out.write('Category\tScore\n')
            for data in first:
                out.write(data + '\t' + str(first.get(data)) + '\n')
        out.close()
        with open('output/Frequent Reviewers.tsv', 'w') as out:
            out.write('Category\tScore\n')
            for data in frequent:
                out.write(data + '\t' + str(frequent.get(data)) + '\n')
        out.close()
        with open('output/Average Ratings.tsv', 'w') as out:
            out.write('Category\tScore\n')
            out.write('First positive' + '\t' + str(float(positive.get('first')) / float(pf1)) + '\n')
            out.write('Frequent positive' + '\t' + str(float(positive.get('frequent')) / float(pf2)) + '\n')
            out.write('First negative' + '\t' + str(float(negative.get('first')) / float(nf1)) + '\n')
            out.write('Frequent negative' + '\t' + str(float(negative.get('frequent')) / float(nf2)) + '\n')
            out.write('First neutral' + '\t' + str(float(neutral.get('first')) / float(ne1)) + '\n')
            out.write('Frequent neutral' + '\t' + str(float(neutral.get('frequent')) / float(ne2)) + '\n')
        out.close()
        with open('output/Ratings comparison.tsv','w') as out:
            out.write('Category\tScore\n')
            for data in ratings_new:
                out.write('New ' + data + '\t' + str(ratings_new.get(data)) + '\n')
            for data in ratings_frequent:
                out.write('Frequent ' + data + '\t' + str(ratings_frequent.get(data)) + '\n')
    return


def year_analysis():
    year_review = {}
    day_review = {}
    helpful_year = {}
    helpful_day = {}
    with open('movies.csv','r') as movie:
        reader = csv.reader(movie.read().splitlines())
        header = reader.next()
        for row in reader:
            time = row[5].rstrip()
            split_score = row[3].rstrip().split('/')
            if split_score[1] == '0':
                split_score[1] = '1'
            help_score = float(split_score[0])/float(split_score[1])
            #print help_score
            year = dt.datetime.fromtimestamp(int(time)).strftime('%Y')
            months = dt.datetime.fromtimestamp(int(time)).strftime('%m')
            date1 = dt.datetime.fromtimestamp(int(time)).strftime('%d')
            date_obj = dt.date(int(year),int(months),int(date1))
            days = dt.date.isoweekday(date_obj)
            day_name = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            text = row[6].rstrip().split()
            summ = 0
            count = 0
            for data in text:
                if words.has_key(data) and words.get(data) != 0:
                    summ += int(words.get(data))
                    count += 1
            if count == 0:
                count = 1
            val = float(summ) / float(count)
            if val > 0:
                if year_review.has_key(year + '-positive'):
                    year_review[year + '-positive'] = year_review.get(year + '-positive') + 1
                else:
                    year_review[year + '-positive'] = 1
                if day_review.has_key(day_name[days-1] + '-positive'):
                    day_review[day_name[days-1] + '-positive'] = day_review.get(day_name[days-1] + '-positive') + 1
                else:
                    day_review[day_name[days-1] + '-positive'] = 1
            elif val < 0:
                if year_review.has_key(year + '-negative'):
                    year_review[year + '-negative'] = year_review.get(year + '-negative') + 1
                else:
                    year_review[year + '-negative'] = 1
                if day_review.has_key(day_name[days-1] + '-negative'):
                    day_review[day_name[days-1] + '-negative'] = day_review.get(day_name[days-1] + '-negative') + 1
                else:
                    day_review[day_name[days-1] + '-negative'] = 1
            else:
                if year_review.has_key(year + '-neutral'):
                    year_review[year + '-neutral'] = year_review.get(year + '-neutral') + 1
                else:
                    year_review[year + '-neutral'] = 1
                if day_review.has_key(day_name[days-1] + '-neutral'):
                    day_review[day_name[days-1] + '-neutral'] = day_review.get(day_name[days-1] + '-neutral') + 1
                else:
                    day_review[day_name[days-1] + '-neutral'] =  1
            if val>0 and help_score>0.5:
                if helpful_year.has_key(year + '-positive-yes'):
                    helpful_year[year + '-positive-yes'] = helpful_year.get(year + '-positive-yes') + 1
                else:
                    helpful_year[year + '-positive-yes'] = 1
                if helpful_day.has_key(day_name[days-1] + '-positive-yes'):
                    helpful_day[day_name[days-1] + '-positive-yes'] = helpful_day.get(day_name[days-1] + '-positive-yes') + 1
                else:
                    helpful_day[day_name[days-1] + '-positive-yes'] = 1
            elif val>0 and help_score<=0.5:
                if helpful_year.has_key(year + '-positive-no'):
                    helpful_year[year + '-positive-no'] = helpful_year.get(year + '-positive-no') + 1
                else:
                    helpful_year[year + '-positive-no'] = 1
                if helpful_day.has_key(day_name[days-1] + '-positive-no'):
                    helpful_day[day_name[days-1] + '-positive-no'] = helpful_day.get(day_name[days-1] + '-positive-no') + 1
                else:
                    helpful_day[day_name[days-1] + '-positive-no'] = 1
            elif val<0 and help_score>0.5:
                if helpful_year.has_key(year + '-negative-yes'):
                    helpful_year[year + '-negative-yes'] = helpful_year.get(year + '-negative-yes') + 1
                else:
                    helpful_year[year + '-negative-yes'] = 1
                if helpful_day.has_key(day_name[days-1] + '-negative-yes'):
                    helpful_day[day_name[days-1] + '-negative-yes'] = helpful_day.get(day_name[days-1] + '-negative-yes') + 1
                else:
                    helpful_day[day_name[days-1] + '-negative-yes'] = 1
            elif val<0 and help_score<=0.5:
                if helpful_year.has_key(year + '-negative-no'):
                    helpful_year[year + '-negative-no'] = helpful_year.get(year + '-negative-no') + 1
                else:
                    helpful_year[year + '-negative-no'] = 1
                if helpful_day.has_key(day_name[days-1] + '-negative-no'):
                    helpful_day[day_name[days-1] + '-negative-no'] = helpful_day.get(day_name[days-1] + '-negative-no') + 1
                else:
                    helpful_day[day_name[days-1] + '-negative-no'] = 1
            elif val==0 and help_score>0.5:
                if helpful_year.has_key(year + '-neutral-yes'):
                    helpful_year[year + '-neutral-yes'] = helpful_year.get(year + '-neutral-yes') + 1
                else:
                    helpful_year[year + '-neutral-yes'] = 1
                if helpful_day.has_key(day_name[days-1] + '-neutral-yes'):
                    helpful_day[day_name[days-1] + '-neutral-yes'] = helpful_day.get(day_name[days-1] + '-neutral-yes') + 1
                else:
                    helpful_day[day_name[days-1] + '-neutral-yes'] = 1
            elif val==0 and help_score<=0.5:
                if helpful_year.has_key(year + '-neutral-no'):
                    helpful_year[year + '-neutral-no'] = helpful_year.get(year + '-neutral-no') + 1
                else:
                    helpful_year[year + '-neutral-no'] = 1
                if helpful_day.has_key(day_name[days-1] + '-neutral-no'):
                    helpful_day[day_name[days-1] + '-neutral-no'] = helpful_day.get(day_name[days-1] + '-neutral-no') + 1
                else:
                    helpful_day[day_name[days-1] + '-neutral-no'] = 1
    movie.close()
    with open('output/Year-Reviews.tsv','w') as out:
        out.write('Category\tCount\n')
        for data in year_review:
            out.write(data + '\t' + str(year_review.get(data)) + '\n')
    out.close()
    with open('output/Day-Reviews.tsv','w') as out:
        out.write('Category\tCount\n')
        for data in day_review:
            out.write(data + '\t' + str(day_review.get(data)) + '\n')
    out.close()
    with open('output/Day-Helpful.tsv','w') as out:
        out.write('Category\tCount\n')
        for data in helpful_day:
            out.write(data + '\t' + str(helpful_day.get(data)) + '\n')
    out.close()
    with open('output/Year-Helpful.tsv','w') as out:
        out.write('Category\tCount\n')
        for data in helpful_year:
            out.write(data + '\t' + str(helpful_year.get(data)) + '\n')
    out.close()
    return

create_initial()
top_rated_movies()
review_sentiment()
year_analysis()