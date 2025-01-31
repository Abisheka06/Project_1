import streamlit as st

import pandas as pd

import pycountry

from Scripts.dbconnection_project1 import dbread

from Scripts.dbconnection_project1 import dbreadWithColumnNames

from Scripts.dbconnection_project1 import dbwrite

with st.sidebar:
        add_text=st.markdown("""
                # Toggle between screens to access more data.
        """)

page = st.sidebar.selectbox("Navigate", ["Home: Competitors", "Venues and Complexes", "Competitions and Categories"])

# Page content
if page == "Home: Competitors":
    st.title('🎾 Tennis Data Analysis')

    row1 = st.columns(3)

    tile1 = row1[0].container(height=120)
    tile2 = row1[1].container(height=120)
    tile3 = row1[2].container(height=120)

    tile1.text("Total number of competitors.")
    tile2.text("Number of countries represented.")
    tile3.text("Highest points scored by a competitor.")

    value= dbread("select count(1) from competitors")

    if value:
        txt1=value[0][0]

    tile1.text(txt1)

    value1= dbread("select count(distinct country) from competitors")

    if value1:
        txt2=value1[0][0]

    tile2.text(txt2)

    value2= dbread("select max(points) from competitor_rankings")

    if value2:
        txt3=value2[0][0]

    tile3.text(txt3)

    with st.sidebar:
        add_text=st.markdown("""
            # Search competitors by Name
        """)

        query = "SELECT name FROM competitors"
        rows=dbread(query)
        column_data = []
        for row in rows:
            column_data.append(row[0])

        add_name=st.selectbox("Select Competitor",column_data)

        data,column_names=dbreadWithColumnNames("select c.name,c.country,c.abbreviation,cr.Comp_rank,cr.points from competitors as c inner join competitor_rankings as cr on c.competitor_id = cr.competitor_id WHERE c.name = '"+add_name+"'")


    st.title("About: "+add_name)
    df = pd.DataFrame(data, columns=column_names)

    st.dataframe(df,width=800,height=50)
    

    countries = [country.name for country in pycountry.countries]

    with st.sidebar:
        add_text=st.markdown("""
                # Filter
        """)

        options = ["All"] + sorted(countries)

        add_country=st.selectbox("Select Country",options,index=0)

        min_rank,max_rank=st.slider("Rank",min_value=0,max_value=500,value=(0,500))

        fil_data,col_names=dbreadWithColumnNames("select c.name,c.country,c.abbreviation,cr.Comp_rank,cr.points from competitors as c inner join competitor_rankings as cr on c.competitor_id = cr.competitor_id where c.country= '"+add_country+"'and cr.Comp_rank between "+str(min_rank)+" and "+str(max_rank))

        df,col=dbreadWithColumnNames("select c.name,c.country,c.abbreviation,cr.Comp_rank,cr.points from competitors as c inner join competitor_rankings as cr on c.competitor_id = cr.competitor_id")

    st.title("Data after applying filter!!!")

    if add_country=="All":
        aldf=pd.DataFrame(df,columns=col)
        st.dataframe(aldf, width=800, height=200)
    else:
        fil_datadf=pd.DataFrame(fil_data,columns=col_names)
        st.dataframe(fil_datadf,width=800,height=400)

elif page == "Venues and Complexes":
    st.title('🎾 Venues and Complexes')

    row1 = st.columns(2)

    tile1 = row1[0].container(height=120)
    tile2 = row1[1].container(height=120)
    

    tile1.text("Total number of Complexes.")
    tile2.text("Number of Venues.")

    value= dbread("select count(distinct complex_name) from complexes")

    if value:
        txt1=value[0][0]

    tile1.text(txt1)

    value1= dbread("select count(distinct venue_name) from venues")

    if value:
        txt2=value1[0][0]

    tile2.text(txt2)

    countries = [country.name for country in pycountry.countries]

    with st.sidebar:
        add_text=st.markdown("""
                # Filter
        """)

        options = ["All"] + sorted(countries)

        add_country=st.selectbox("Select Country",options,index=0)

        add_text=st.markdown("""
            # Complexes
        """)

        if add_country == "All":
            query = "SELECT complex_name FROM complexes"
        else:
            query = "select distinct c.complex_name from complexes as c inner join venues as v on c.complex_id = v.complex_id where v.country_name='"+add_country+"'"
        
        rows=dbread(query)
        column_data = []
        for row in rows:
            column_data.append(row[0])

        options1=["All"] + sorted(column_data)

        add_complex=st.selectbox("Select Complexes",options1,index=0)
    
    data,col_name=dbreadWithColumnNames("select v.country_name,c.complex_name,v.Venue_name,v.timezone from complexes as c inner join venues as v on c.complex_id = v.complex_id")

    data_complex,column_names=dbreadWithColumnNames("select v.country_name,c.complex_name,v.Venue_name,v.timezone from complexes as c inner join venues as v on c.complex_id = v.complex_id where v.country_name='"+add_country+"'")

    data_notall,columns=dbreadWithColumnNames("select v.country_name,c.complex_name,v.Venue_name,v.timezone from complexes as c inner join venues as v on c.complex_id = v.complex_id where v.country_name='"+add_country+"' and c.complex_name='"+add_complex+"'")

    data_last,col=dbreadWithColumnNames("select v.country_name,c.complex_name,v.Venue_name,v.timezone from complexes as c inner join venues as v on c.complex_id = v.complex_id where c.complex_name='"+add_complex+"'")

    st.title("Complexes and Venues data after applying filter!!")

    if add_country == "All" and add_complex == "All":
        aldf=pd.DataFrame(data,columns=col_name)
        st.dataframe(aldf, width=800, height=200)

    elif add_complex == "All" and add_country != "All":
        comp_data=pd.DataFrame(data_complex,columns=column_names)
        st.dataframe(comp_data, width=800, height=200)

    elif add_complex != "All" and add_country != "All":
        comp=pd.DataFrame(data_notall,columns=columns)
        st.dataframe(comp, width=800, height=200)

    else:
        compl=pd.DataFrame(data_last,columns=col)
        st.dataframe(compl, width=800, height=200)

if page == "Competitions and Categories":
    st.title('🎾 Competitions and Categories Data')

    st.header('Number of competitions in each type')

    row1 = st.columns(3)

    tile1 = row1[0].container(height=120)
    tile2 = row1[1].container(height=120)
    tile3 = row1[2].container(height=120)

    tile1.text("Singles")
    tile2.text("Doubles")
    tile3.text("Mixed")

    value= dbread("select count(*) from competitions where type = 'singles'")

    if value:
        txt1=value[0][0]

    tile1.text(txt1)

    value1= dbread("select count(*) from competitions where type = 'doubles'")

    if value1:
        txt2=value1[0][0]

    tile2.text(txt2)

    value2= dbread("select count(*) from competitions where type = 'mixed'")

    if value2:
        txt3=value2[0][0]

    tile3.text(txt3)

    with st.sidebar:
        add_text=st.markdown("""
                # Search by Gender
        """)

        options = ["Men","Women"]

        add_gender=st.selectbox("Select Gender",options,index=0)

    # data,col_name=dbreadWithColumnNames("select cp.competition_name, cp.gender, cp.type, cg.category_name from competitions as cp inner join categories as cg on cp.category_id = cg.category_id")

    st.title("Competitions for "+add_gender)
    data_complex,column_names=dbreadWithColumnNames("select cp.competition_name, cp.gender, cp.type, cg.category_name from competitions as cp inner join categories as cg on cp.category_id = cg.category_id where cp.gender='"+add_gender+"' limit 500")

    gen_data=pd.DataFrame(data_complex,columns=column_names)
    st.dataframe(gen_data, width=800, height=200)







    


    
        





    