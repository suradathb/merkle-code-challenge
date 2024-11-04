# Implementation:

### Q) What libraries did you add to the frontend? What are they used for?
React: ใช้สำหรับสร้าง UI ที่เป็น component-based
Axios: ใช้สำหรับทำ HTTP requests เพื่อดึงข้อมูลจาก API
React Router: ใช้สำหรับการจัดการ routing ในแอปพลิเคชัน
Styled-components: ใช้สำหรับการเขียน CSS ในรูปแบบ JavaScript

### Q) What's the command to start the frontend application locally?
npm run dev


### Q) What libraries did you add to the backend? What are they used for?
ในส่วน backend ที่ใช้ FastAPI ผมเพิ่มไลบรารีดังนี้:

FastAPI: ใช้สำหรับสร้างเว็บแอปพลิเคชันที่มีประสิทธิภาพสูงและรองรับการทำงานแบบ asynchronous
uvicorn: ใช้เป็น ASGI server สำหรับรันแอปพลิเคชัน FastAPI
SQLAlchemy: ใช้สำหรับการเชื่อมต่อและจัดการฐานข้อมูล
pydantic: ใช้สำหรับการตรวจสอบและการจัดการข้อมูลที่รับเข้ามาใน API
httpx: ใช้สำหรับทำ HTTP requests เพื่อดึงข้อมูลจาก API ภายนอก

### Q) What's the command to start the backend application locally?
uvicorn app.main:app --reload --port 4000
---

# General:

### Q) If you had more time, what further improvements or new features would you add?
ถ้ามีเวลามากกว่านี้ ผมจะเพิ่มฟีเจอร์การแสดงผลกราฟสำหรับข้อมูลราคาของ cryptocurrencies และเพิ่มระบบการแจ้งเตือนเมื่อราคามีการเปลี่ยนแปลงอย่างมีนัยสำคัญ
### Q) Which parts are you most proud of? And why?
ผมภูมิใจในส่วนของการสร้าง API ที่สามารถดึงข้อมูลจากหลายแหล่งและคำนวณราคาที่ดีที่สุดได้ เพราะมันแสดงถึงความสามารถในการจัดการกับข้อมูลและการประมวลผลที่ซับซ้อน
### Q) Which parts did you spend the most time with? What did you find most difficult?
ส่วนที่ใช้เวลามากที่สุดคือการทำให้ frontend มีการแสดงผลที่ responsive และการจัดการกับการกรองและเรียงลำดับข้อมูล ซึ่งเป็นส่วนที่ยากที่สุดเพราะต้องใช้การประสานงานระหว่างหลาย component และการจัดการ state ที่ซับซ้อน
### Q) How did you find the test overall? Did you have any issues or have difficulties completing?If you have any suggestions on how we can improve the test, we'd love to hear them.
โดยรวมแล้วการทดสอบนี้เป็นประสบการณ์ที่ดีและท้าทาย ผมได้เรียนรู้และฝึกฝนทักษะหลายอย่าง อย่างไรก็ตาม การจัดการกับ API หลายแหล่งและการทำให้ frontend responsive เป็นส่วนที่ท้าทายที่สุด ถ้ามีข้อเสนอแนะ ผมคิดว่าการเพิ่มคำแนะนำหรือเอกสารเพิ่มเติมเกี่ยวกับการใช้งาน API จะช่วยให้การทดสอบนี้ง่ายขึ้น