select rp1.choice_id, rp2.choice_id, count(rp1.person_id) 
from questions_response rp1 outer join questions_response rp2 on rp1.person_id=rp2.person_id
where rp1.poll_id=11 
and rp2.poll_id=13 
group  by 1,2;


cursor.execute("select rp1.choice_id, rp2.choice_id, count(rp1.person_id) from questions_response as rp1 left join questions_response as rp2 on rp1.person_id=rp2.person_id where rp1.poll_id=11 and rp2.poll_id=13  group  by 1,2")
