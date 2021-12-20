from numpy import record
import streamlit as st
import mysql.connector 
import pandas as pd
from mysql.connector.errors import Error
from mysql_connection import get_connection

## 이렇게 쿼리문을 여러개 작성할때도 connection은 한번만하고
## connection.close도 맨 끝에 한번만 한다.


def run_select_app() :
    st.subheader('데이터 조회')

    try : 
        connection = get_connection()
        
        query = '''select id, email, age, address, created_at from test_user'''

        # select 결과를 딕셔너리로 가져온다
        cursor = connection.cursor(dictionary = True)

        cursor.execute(query)

        # select 문은 아래 내용이 필요하다.
        # 커서로 부터 실행한 결과 전부를 받아와라.
        record_list = cursor.fetchall()
        print(record_list)

        # select 문구를 화면에 표시해보자
        df = pd.DataFrame(data = record_list)
        df.index += 1 
        if df['id'].isna().sum() == 0 :  
            st.dataframe(df)
            
        else : 
            st.write('저장된 id가 없습니다.')


        # id 로 검색해 보자
        st.subheader('아이디로 조회')
        search_id = st.number_input('검색할 아이디를 선택하세요',min_value=1)
        query = '''select id, email, age, address, created_at from test_user where id = %s'''
        param = (search_id, )
        
        cursor.execute(query, param)
        record_list = cursor.fetchall()
        print(record_list)

        # select 문구를 화면에 표시해보자
        df_id = pd.DataFrame(data = record_list)
        #df_id.set_index = ['id']
        if df_id.shape != (0,0) :  
            st.dataframe(df_id)
            print(df_id.shape)
        else : 
            st.write('검색하신 id가 없습니다.')


        # 이메일로 검색해 보자.
        st.subheader('이메일로 조회')
        search_email = st.text_input('검색할 이메일을 적어주세요')
        

        

        print('이메일 검색어', search_email)

        if st.button('검색하기!') :
            query = '''select id, email, age, address, created_at from test_user where email like %s '''
            search_email = "%" + search_email + "%"
            print(search_email)
            param = (search_email, )
            
            cursor.execute(query, param)
            record_list = cursor.fetchall()
            print(record_list)
            # select 문구를 화면에 표시해보자
            df_email = pd.DataFrame(data = record_list)
            df_email.index += 1            
            if df_email.shape != (0,0) and len(search_email)>2 :  
                st.dataframe(df_email)
                print('email shape : ',df_email.shape)
            else : 
                st.write('검색하신 이메일이 없습니다.')




    # 위의 코드를 실행하다가, 문제가 생기면, except를 실행하라는 뜻.
    except Error as e :
        # 뒤의 e는 에러를 찍어라 error를 e로 저장했으니까!
        print('Error while connecting to MySQL', e)
    # finally 는 try에서 에러가 나든 안나든, 무조건 실행하라는 뜻.
    finally : 
        print('finally')
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL connection is closed')
        else :
            print('connection does not exist') 
        