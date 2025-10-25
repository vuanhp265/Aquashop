import React, { useEffect, useState } from 'react';

function App(){
  const [fish, setFish] = useState([]);
  const [accessories, setAccessories] = useState([]);
  const [orders, setOrders] = useState([]);

  useEffect(()=>{
    fetch('/api/fish').then(r=>r.json()).then(setFish);
    fetch('/api/accessories').then(r=>r.json()).then(setAccessories);
    fetch('/api/orders').then(r=>r.json()).then(setOrders);
  },[]);

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>AquaShop - Quản lý bán cá cảnh & phụ kiện</h1>
      <section>
        <h2>Danh sách cá</h2>
        <ul>{fish.map(f=> <li key={f.id}>{f.name} — {f.species} — {f.price}₫ — stock: {f.stock}</li>)}</ul>
      </section>
      <section>
        <h2>Danh sách phụ kiện</h2>
        <ul>{accessories.map(a=> <li key={a.id}>{a.name} — {a.category} — {a.price}₫ — stock: {a.stock}</li>)}</ul>
      </section>
      <section>
        <h2>Đơn hàng gần đây</h2>
        <ul>{orders.map(o=> <li key={o.id}>{o.customer_name} — {o.total}₫ — {o.status}</li>)}</ul>
      </section>
      <p>Ghi chú: frontend giả lập gọi API từ cùng domain; khi chạy dev, bạn có thể proxy hoặc chạy backend trên port 5000 và frontend trên 3000 with proxy setting.</p>
    </div>
  );
}

export default App;
