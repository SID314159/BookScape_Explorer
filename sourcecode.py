import pandas as pd
import streamlit as st
import requests
import json
searchlist=["python","datascience","java","c programming", "sql",
            "c++ programming", "HTML", "CSS", "javascript", "computer science", 
            "physics", "blackhole", "artificial intelligence", "machine learning", "statistics",
            "quantum computing", "probability", "calculus", "gravity", "arithmetics",
            "geometry","Artificial General Intelligence", "tensorflow", "differential equations","embedded programming",
            "thermodynamics","atoms","biology","magnetism", "chemical"] #default searchlist

if "searchlist1" not in st.session_state: #user input searchlist
    st.session_state.searchlist1=["python","datascience","java","c programming", "sql",
            "c++ programming", "HTML", "CSS", "javascript", "computer science", 
            "physics", "blackhole", "artificial intelligence", "machine learning", "statistics",
            "quantum computing", "probability", "calculus", "gravity", "arithmetics",
            "geometry","Artificial General Intelligence", "tensorflow", "differential equations","embedded programming",
            "thermodynamics","atoms","biology","magnetism", "chemical"]

def datclt(searchkey):   #function to collect data and return dlist
    skdct={}
    tdlist=[] # used in while loop to collect data for each searchkey
    dlist=[]  #Combined "items" of all pagenation to dlist
    #JSON pattern - (d["items"][i]["volumeInfo"]["title"]) pattern of the JSON
    i=0 #for while loop
    for j in range(0, len(searchkey)): #iterates through each book title given in search key list
        while len(tdlist)<120:    #collects 1000 data for each searchkey and appends only the "items" list of each pagenation into tdlist
            url="https://www.googleapis.com/books/v1/volumes?"
            parameters={
                "q": searchkey[j],
                "key":"AIzaSyAlqinZpRTufEeF8zV0kxecdi6HasQQyKMMD",
                "startIndex":0,
                "maxResults":40
            }
            try:
                data=requests.get(url,params=parameters).json()
                with open (r"G:\DS\guvi\Projects\Ver2.0\ProjectBookscapeExplorer\code\jsonbooks.json","a") as file:
                    json.dump(data,file,indent=4)
                    file.close()
                if "items" in data: 
                    tdlist.extend(data["items"])
                    # print(len(tdlist))
                    
                else:
                    print(f"no more data on DB {j}, collecting data for {searchkey[j+1]} ")
                    break       
            except requests.exceptions.RequestException as e:
                print(e)
                break
            i+=40
        dlist.extend(tdlist)
        print(len(dlist))
        
        skdct[f"{searchkey[j]}"]=len(tdlist)
        itm=list(skdct.items()) 

        tdlist=[]

     #writing to file for documentation   
    with open (r"G:\DS\guvi\Projects\Ver2.0\ProjectBookscapeExplorer\code\10001books.json","w") as file:
        json.dump(dlist,file,indent=4)
        file.close()

# #fetching schema from file & writing DB
# with open (r"G:\DS\guvi\Projects\Ver2.0\ProjectBookscapeExplorer\code\1000books.json","r") as file:
#     dlist= json.load(file)
    print(itm)
    print(f"{len(dlist)} books data found" ) 
    count=0  #counts the for loop iteration
    dfdict={"book_id":[],                                #final dictionary to be written in DB
            "search_key":[],
            "book_title":[],
            "book_subtitle":[],
            "book_authors":[],
            "total_authors":[],
            "book_description":[],
            "industryIdentifiers":[],
            "text_readingModes":[],
            "image_readingModes":[],
            "pageCount":[],
            "categories":[],
            "language":[],
            "imageLinks":[],
            "ratingsCount":[],
            "averageRating":[],
            "country":[],
            "saleability":[],
            "isEbook":[],
            "amount_listPrice":[],
            "currencyCode_listPrice":[],
            "amount_retailPrice":[],
            "Discount_percentage":[],
            "currencyCode_retailPrice":[],
            "buyLink":[],
            "year":[],
            "publisher":[]

            }
    k=0 # for searchkey loop
    m=0 #for searchkey loop
    for i in range(0, len(dlist)):

        id=dlist[i].get("id","NA")
        dfdict['book_id'].append(id)

        if k < itm[m][1]:
            dfdict['search_key'].append(itm[m][0])
            k+=1

        else:
            k=0
            m+=1
            dfdict['search_key'].append(itm[m][0])
            k+=1

        
        title=dlist[i]["volumeInfo"].get("title","NA")
        dfdict["book_title"].append(title)

        subtitle=dlist[i]["volumeInfo"].get("subtitle","NA")
        dfdict["book_subtitle"].append(subtitle)

        authors=dlist[i]["volumeInfo"].get("authors","NA")
        if isinstance(authors, list):
            l=len(authors)
            authors=", ".join(authors)
            dfdict["book_authors"].append(authors)
            dfdict["total_authors"].append(l)
            
        else:
            dfdict["book_authors"].append(authors)
            dfdict["total_authors"].append(1)

        description=dlist[i]["volumeInfo"].get("description","NA")
        dfdict["book_description"].append(description)

        identifier=dlist[i]["volumeInfo"].get("industryIdentifiers","NA")
        if identifier!="NA":
            identifier=identifier[0].get("identifier","NA")
        dfdict["industryIdentifiers"].append(identifier)

        text=dlist[i]["volumeInfo"]["readingModes"].get("text","NA")
        dfdict["text_readingModes"].append(text)

        image=dlist[i]["volumeInfo"]["readingModes"].get("image","NA")
        dfdict["image_readingModes"].append(image)

        pageCount=dlist[i]["volumeInfo"].get("pageCount","NA")
        dfdict["pageCount"].append(pageCount)

        categories=dlist[i]["volumeInfo"].get("categories","NA")
        if isinstance(categories, list):
            categories=", ".join(categories)
            dfdict["categories"].append(categories)
        else:
            dfdict["categories"].append(categories)

        language=dlist[i]["volumeInfo"].get("language","NA")
        dfdict["language"].append(language)

        imageLinks=dlist[i]["volumeInfo"].get("imageLinks","NA")
        if imageLinks!="NA":
            imageLinks=imageLinks.get("thumbnail","NA")
        dfdict["imageLinks"].append(imageLinks)

        ratingsCount=dlist[i]["volumeInfo"].get("ratingsCount","NA")
        dfdict["ratingsCount"].append(ratingsCount)

        averageRating=dlist[i]["volumeInfo"].get("averageRating","NA")
        dfdict["averageRating"].append(averageRating)

        country=dlist[i]["saleInfo"].get("country","NA")
        dfdict["country"].append(country)

        saleability=dlist[i]["saleInfo"].get("saleability","NA")
        dfdict["saleability"].append(saleability)

        isEbook=dlist[i]["saleInfo"].get("isEbook","NA")
        if isEbook== True:
            dfdict["isEbook"].append(1)
        else:
            dfdict["isEbook"].append(0)


        amount=dlist[i]["saleInfo"].get("listPrice","NA")
        if amount!="NA":
            amount=amount.get("amount","NA")
        dfdict["amount_listPrice"].append(amount)

        currencyCode=dlist[i]["saleInfo"].get("listPrice","NA")
        if currencyCode!="NA":
            currencyCode=currencyCode.get("currencyCode","NA")
        dfdict["currencyCode_listPrice"].append(currencyCode)
        
        amount=dlist[i]["saleInfo"].get("retailPrice","NA")
        if amount!="NA":
            amount=amount.get("amount","NA")
        dfdict["amount_retailPrice"].append(amount)

        currencyCode=dlist[i]["saleInfo"].get("retailPrice","NA")
        if currencyCode!="NA":
            currencyCode=currencyCode.get("currencyCode","NA")
        dfdict["currencyCode_retailPrice"].append(currencyCode)

        amount_lp=0
        amount_rp=0
        amount=dlist[i]["saleInfo"].get("listPrice","NA")
        if amount!="NA":
            amount_lp=float(amount.get("amount",0))
   
        amount=dlist[i]["saleInfo"].get("retailPrice","NA")
        if amount!="NA":
            amount_rp=float(amount.get("amount",0))
        if amount_lp!=0 and amount_rp!=0:
            percentage=int(round((amount_rp/amount_lp)*100))
            dfdict["Discount_percentage"].append(percentage)
        else:
            dfdict["Discount_percentage"].append("NA")


        buyLink=dlist[i]["saleInfo"].get("buyLink","NA")
        dfdict["buyLink"].append(buyLink)

        publishedDate=dlist[i]["volumeInfo"].get("publishedDate","NA")
        year=publishedDate[0:4]
        dfdict["year"].append(year)

        publisher=dlist[i]["volumeInfo"].get("publisher","NA")
        dfdict["publisher"].append(publisher)

        count+=1  #represents the iteration through each book in tdlist(each dictionary in "items" list)

    dbdf_dup=pd.DataFrame(dfdict) 
    dbdf = dbdf_dup.drop_duplicates(subset='book_title', keep='first') 
    print(f"{count} rows inserted")
    print(dbdf)  
    print(dbdf.shape)
    return(dbdf)
        
def sql_upload(dtframe):   #writing the dataframes of searchkey or streamlit keyword into sql using pymysql+sqlalchemy

    from sqlalchemy import create_engine, URL,exc, Integer

    connect_args = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": r"G:\DS\guvi\Projects\Ver2.0\ProjectBookscapeExplorer\code\TIDB_Certificate\isrgrootx1.pem",
        }
     
    engine = create_engine(
            URL.create(
            drivername="mysql+pymysql",
            username="3LHApunfAprgwZ4.root",
            password="UTR1eix9QCrXfwML",
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            database="BookScape_Explorer",
        ), connect_args=connect_args)
    
    

    try:
        #columntype={"ratingsCount": Integer}
        dtframe.to_sql(
            name="Books",       # Table name
            con=engine,              # SQLAlchemy engine
            if_exists="append",     # Options: 'fail', 'replace', 'append'
            index=False,             # Do not write the DataFrame index as a column
            #dtype=columntype
        )

    except exc.SQLAlchemyError as e:
      print(e)

    finally:
      engine.dispose()
      print("Engine closed")
      return True

def dbcall(qpass, params=None): # passing streamlit return to our DB and getting return
    import pymysql
    from pymysql import Error
    try:
        connection = pymysql.connect(
        host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port = 4000,
        user = "3LHApunfAprgwZ4.root",
        password = "UTR1eix9QCrXfwML",
        database = "BookScape_Explorer",
        ssl_ca= r"G:\DS\guvi\Projects\Ver2.0\ProjectBookscapeExplorer\code\TIDB_Certificate\isrgrootx1.pem")
        print(connection)

        if connection:
            cursor=connection.cursor()
            cursor.execute(qpass,params)
            ans=cursor.fetchall()
            

    except Error as e:
        print(e)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed")
            return(ans)
 

########Streamlit Attributes##########
import streamlit as st
import pandas as pd
       
qlist={       # defining questions and their sql queries for easy updation in future
    
    "Availability of eBooks vs Physical Books":"select count(*) from Books where isEbook=1",#0
    "Publisher with the Most Books Published":"select publisher, count(*) as total from Books where publisher!='NA' group by publisher order by total desc limit 1",   #1
    "Publishers with Highest Average Rating":"select publisher, averageRating from books where averageRating=5 and publisher!='NA' group by averageRating, publisher order by averageRating desc", #2
    "Top 5 Most Expensive Books by Retail Price":"select book_title, amount_retailPrice from Books where amount_retailPrice!= 'NA' order by amount_retailPrice desc limit 5", #3
    "Books Published After 2010 with at Least 500 Pages":"select book_title, year, pageCount from Books where year>=2010 and pageCount>=500 order by year", #4
    "Books with Discounts Greater than 20%": "select book_title, Discount_percentage as Discount from Books where Discount_percentage>20 order by Discount_percentage desc", #5
    "Average Page Count for eBooks vs Physical Books": """select case 
        when isEbook=1 then 'E-Book'
        when isEbook=0 then 'Physical Book' end as 'Book Types', round(avg(pageCount))
        from Books group by isEbook""", #6
    "Top 3 Authors with the Most Books":"select book_authors from books group by book_authors order by 'Total Books' desc", #7
    "Publishers with More than 10 Books":"select publisher, count(book_title) as 'Total' from books where publisher!='NA' group by publisher having Total > 10 order by Total", #8
    "Average Page Count for Each Category":"select categories,round(avg(pageCount)) as 'Avg' from Books where pageCount!=0 group by categories order by Avg desc", #9
    "Books with More than 3 Authors":"select book_title, book_authors, total_authors from books where total_authors > 3 order by total_authors", #10
    "Ratings Count Greater Than the Average": "select book_title,ratingsCount from books where ratingsCount>(select round(avg(ratingsCount)) from books where ratingsCount!='NA' order by ratingsCount) order by ratingsCount", #11
    "Books with the Same Author Published in the Same Year":"select book_title,book_authors,year from (select book_title,book_authors,year, count(*) over(partition by book_authors, year) as 'BC' from books)temptable where BC>1 and book_authors!='NA' and year!='NA'", #12
    "Books with a Specific Keyword in the Title":"select search_key, book_title from books", #13
    "Year with the Highest Average Book Price":"select year, count(book_title), round(avg(amount_retailPrice)) as 'Avg. Price' from books group by year order by round(avg(amount_retailPrice)) desc limit 1", #14
    "Count Authors Who Published 3 Consecutive Years":"select  book_authors, count(year) as Total from books where year!='NA' and book_authors!='NA' group by book_authors having Total>=3", #15
    "Authors who have published books in the same year but under different publishers":"select book_authors, year, count(publisher) from (select book_authors, year, publisher, count(book_title) from books group by book_authors, year, publisher order by count(book_title) desc) temptble where book_authors!='NA' group by book_authors, year having count(publisher)>1", #16
    "Average amount_retailPrice of eBooks and physical books":"select isEbook,round(avg(amount_retailPrice)) from books group by isEbook order by isEbook ", #17
    "Books with averageRating that is more than two standard deviations away from the average rating of all books":"select round(avg(averageRating)), stddev(averageRating) from books where averageRating!='NA' ", #18
    "Publishers with more than 10 books and highest average rating among its books":"select publisher, avg(averageRating) as'Avg. Rating', count(*) as 'Total Books' from books where publisher!='NA' and averageRating!='NA' group by publisher having count(*)>10 order by 'Avg. Rating' desc limit 1"
}
keys=qlist.keys()
key=list(keys)


#Streamlit codes
pgrtn=st.sidebar.radio("Menu", ["Data Collector", "Analyzer", "Add Data"])
#page1 
if pgrtn == "Data Collector":
    st.title(":red[Click to collect data]")
    if st.button("Get data"):
        sql_upload(datclt(searchlist))
        st.header(":green[Data collected and stored in Database]")
        
#page2
if pgrtn == "Analyzer":
    qrtn=st.selectbox("Choose Analysis",key) #using the key variable which is list of questions
    if qrtn==key[0]:
        s=dbcall(qlist[key[0]]) #passing corresponding values(SQL queries) for each key(Questions)
        st.write(f"""\nTotal Books: 2000 \n 
                   \nTotal E-Books available: {s[0][0]} \n 
                    \nTotal Physical Books available: {2000-s[0][0]}""")
        
    if qrtn==key[1]:
        s=dbcall(qlist[key[1]])
        st.write(f"{s[0][0]} : {s[0][1]} books")

    if qrtn==key[2]:
        s=pd.DataFrame(dbcall(qlist[key[2]]), columns=["Publisher","Rating"])
        st.write(s)

    if qrtn==key[3]:
        s=pd.DataFrame(dbcall(qlist[key[3]]), columns=["Book","Retail Price"])
        st.write(s)

    if qrtn==key[4]:
        s=pd.DataFrame(dbcall(qlist[key[4]]), columns=["Book","Year","Pages"])
        st.write(f"Total books: {s.shape[0]}")
        st.write(s)

    if qrtn==key[5]:
        s=pd.DataFrame(dbcall(qlist[key[5]]), columns=["Book","Offer in %"])
        st.write(f"Total books: {s.shape[0]}")
        st.write(s)

    if qrtn==key[6]:
        s=pd.DataFrame(dbcall(qlist[key[6]]), columns=["Book Type","Avg. Pages"])
        st.write(s) 

    if qrtn==key[7]:
        ans=dbcall(qlist[key[7]])

        l=[]
        auth=[]
        for i in ans:
          for j in i:
            l.extend(j.split(','))
        from collections import Counter
        d=Counter(l)
        v=list(set(list(d.values())))

        v.sort(reverse=True)
        if len(v)>3:
            lp=3
        else:
            lp=len(v)
            for k in range(0, lp):
                for i in d:
                    if d[i]==v[k]:
                        auth.append([i,v[k]])
        d=pd.DataFrame(auth, columns=["Author","Book_Count"])
        st.write(d) 

    if qrtn==key[8]:
        s=pd.DataFrame(dbcall(qlist[key[8]]), columns=["Publisher","Total Books"])
        st.write(s) 
    
    if qrtn==key[9]:
        s=pd.DataFrame(dbcall(qlist[key[9]]), columns=["Categories","Avg. Page Count"])
        st.write(s)

    if qrtn==key[10]:
        s=pd.DataFrame(dbcall(qlist[key[10]]), columns=["Books","Authors","No. of Authors"])
        st.write(s)   

    if qrtn==key[11]:
        avg=dbcall("select round(avg(ratingsCount)) from books where ratingsCount!='NA'")
        st.write(f"Average Ratings Count: {avg[0][0]}")
        s=pd.DataFrame(dbcall(qlist[key[11]]), columns=["Books","Ratings Count"])
        st.write(s)  

    if qrtn==key[12]:
        s=pd.DataFrame(dbcall(qlist[key[12]]), columns=["Books","Authors","Year"])
        st.write(s) 

    if qrtn==key[13]:
        sk=st.selectbox("Select keyword",st.session_state.searchlist1)
        s=pd.DataFrame(dbcall(qlist[key[13]]), columns=["Keyword","Books"])
        out=s[s["Keyword"]==sk]
        st.write(out)  

    if qrtn==key[14]:
        s=pd.DataFrame(dbcall(qlist[key[14]]), columns=["Year","Total Books","Avg. Price"])
        st.write(s)  

    if qrtn==key[15]:
        s=pd.DataFrame(dbcall(qlist[key[15]]), columns=["Authors","Total"])
        a=s["Authors"].to_list()
        counter=0
        auth=[]
        for i in a:
            y=pd.DataFrame(dbcall("select year from books where book_authors =%s",(i)), columns=["year"])
            y=pd.to_numeric(y["year"],errors="coerce")
            l=y.to_list()
            l.sort()
            count=0
            for j in range (0, (len(l)-3)):
                if l[j+1]-l[j]==1:
                    if l[j+2]-l[j+1]==1:
                        count+=1
                        break
                    else:
                        pass
                else:
                    pass
            if count==1:
                counter+=1
                auth.append(i)
        if counter>0:
            st.write(f"Authors Who Published 3 Consecutive Years: {counter}") 
            st.write(auth) 
        else:
            st.write("No authors Published 3 Consecutive Years")

    if qrtn==key[16]:
        df=pd.DataFrame(dbcall(qlist[key[16]]), columns=["Auth","Year","TotalPub"])
        authors=df["Auth"].to_list()
        years=df["Year"].to_list()

        placeholders = ', '.join(['%s'] * len(authors))
        query = f"""
        select book_authors,year, count(book_title)
        from books
        where book_authors in ({placeholders})
        and year IN ({placeholders}) group by book_authors, year
        """
        param = authors + years

        res = dbcall(query, param)

        ans = pd.DataFrame(res, columns=['Authors', 'Year', 'Total Books'])
        st.write(ans) 

    if qrtn==key[17]:
        s=pd.DataFrame(dbcall(qlist[key[17]]), columns=["a","b"])
        a=s["b"].to_list()

        df=pd.DataFrame([["Physical Book","E-Book"],a])
        st.write(df) 

    if qrtn==key[18]:
        s=dbcall(qlist[key[18]])
        avg=s[0][0]
        std=s[0][1]
        pstd=avg+(2*std)       
        nstd=avg-(2*std)

        st.write(f"Mean: {avg}")
        st.write(f"Standard Deviation: {std}")

        s=pd.DataFrame(dbcall("select book_title, averageRating, ratingsCount from books where averageRating!='NA' and averageRating>%s",(pstd)), columns=["Title", "Avg. Rating",'Ratings Count'])
        st.write(f"Books with Avg. Rating greater than 2 Standard Deviation({pstd})")
        st.write(s)
        s=pd.DataFrame(dbcall("select book_title, averageRating, ratingsCount from books where averageRating!='NA' and averageRating<%s",(nstd)), columns=["Title", "Avg. Rating",'Ratings Count'])
        st.write(f"Books with Avg. Rating lesser than 2 Standard Deviation({nstd})")
        st.write(s)
       
    if qrtn==key[19]:
        s=pd.DataFrame(dbcall(qlist[key[19]]), columns=["Publisher","Avg. Rating","Total Books"])
        st.write(s)  
        
#page3
if pgrtn== "Add Data":
    kwrd=st.text_input("Search Keyword")
    if kwrd in st.session_state.searchlist1:
        st.write(f"Data for {kwrd} already in database")
    else:  
        if st.button("search"):
            #st.write(st.session_state.searchlist1)
            ltemp=[] #temp list to pass argument as list for datclt function
            ltemp.append(kwrd)
            print(ltemp)
            stret=datclt(ltemp) # showing the collected data
            sql_upload(stret)
            st.write(f"Data collected and added for keyword: {kwrd}")
            st.dataframe(stret)
            st.session_state.searchlist1.append(kwrd)  #adds the strmlit passed keyword in searchlist1
            

    




