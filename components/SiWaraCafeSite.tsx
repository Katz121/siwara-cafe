"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MapPin, Phone, ChevronLeft, ChevronRight } from "lucide-react";

export default function SiWaraCafeSite({ mapEmbedSrc }: { mapEmbedSrc?: string }) {
  // --- รายการภาพทั้งหมด ---
  const allImages = [
    "/images/siwara-interior1.jpg",
    "/images/siwara-interior2.jpg",
    "/images/siwara-interior3.jpg",
    "/images/siwara-interior4.jpg",
    "/images/siwara-interior5.jpg",
    "/images/siwara-interior6.jpg",
    "/images/siwara-interior7.jpg",
    "/images/siwara-interior8.jpg",
    "/images/siwara-interior9.jpg",
    "/images/siwara-interior10.jpg",
    "/images/siwara-interior11.jpg",
  ];

  const [images, setImages] = useState<string[]>([]);
  const [badImages, setBadImages] = useState<string[]>([]);
  const [index, setIndex] = useState(0);

  // --- ตรวจสอบว่าภาพไหนโหลดได้ ---
  useEffect(() => {
    Promise.all(
      allImages.map(
        (src) =>
          new Promise<{ ok: boolean; src: string }>((resolve) => {
            const im = new Image();
            im.onload = () => resolve({ ok: true, src });
            im.onerror = () => resolve({ ok: false, src });
            im.src = src;
          })
      )
    ).then((results) => {
      const ok = results.filter(r => r.ok).map(r => r.src);
      const bad = results.filter(r => !r.ok).map(r => r.src);
      setImages(ok.length ? ok : allImages);
      setBadImages(bad);
      if (bad.length) {
        console.warn("[SiWaraCafeSite] รูปโหลดไม่สำเร็จ:", bad);
      }
    });
  }, []);

  // --- ปุ่มเลื่อนสไลด์ ---
  const nextSlide = () => setIndex((i) => (i + 1) % images.length);
  const prevSlide = () => setIndex((i) => (i - 1 + images.length) % images.length);

  // --- Auto slide ---
  useEffect(() => {
    const timer = setInterval(nextSlide, 4000);
    return () => clearInterval(timer);
  }, [images]);

  return (
    <div className="font-sans bg-[#faf6f0] text-[#4a3c2a]">
      {/* HERO */}
      <header
        data-testid="hero"
        className="relative h-[70vh] bg-cover bg-center"
        style={{ backgroundImage: 'url(/images/siwara-hero.jpg)' }}
        aria-label="Si-Wara Café คาเฟ่บ้านไม้ ตะกั่วป่า"
      >
        <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="text-white text-5xl md:text-6xl font-bold drop-shadow-lg text-center"
          >
            Si-Wara Café
          </motion.h1>
        </div>
      </header>

      {/* ABOUT + SLIDER */}
      <section className="max-w-6xl mx-auto py-12 px-6 grid md:grid-cols-2 gap-8 items-center" data-testid="about">
        {/* Slider */}
        <div className="relative overflow-hidden rounded-2xl shadow-lg">
          {images.length > 0 && (
            <AnimatePresence mode="wait">
              <motion.img
                key={index}
                src={images[index]}
                alt={`บรรยากาศภายใน Si-Wara Café ภาพที่ ${index + 1}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.6 }}
                className="w-full h-[350px] md:h-[420px] object-cover"
              />
            </AnimatePresence>
          )}

          {/* ปุ่มเลื่อน */}
          {images.length > 1 && (
            <>
              <button
                onClick={prevSlide}
                aria-label="ภาพก่อนหน้า"
                className="absolute top-1/2 left-4 -translate-y-1/2 bg-black/40 hover:bg-black/60 p-2 rounded-full text-white"
              >
                <ChevronLeft size={22} />
              </button>
              <button
                onClick={nextSlide}
                aria-label="ภาพถัดไป"
                className="absolute top-1/2 right-4 -translate-y-1/2 bg-black/40 hover:bg-black/60 p-2 rounded-full text-white"
              >
                <ChevronRight size={22} />
              </button>
            </>
          )}

          {/* จุดบอกตำแหน่งสไลด์ */}
          {images.length > 1 && (
            <div className="absolute bottom-3 left-0 right-0 flex justify-center gap-2">
              {images.map((_, i) => (
                <span
                  key={i}
                  className={`h-2 w-2 rounded-full ${i === index ? "bg-white" : "bg-white/50"}`}
                />
              ))}
            </div>
          )}
        </div>

        {/* About text */}
        <div>
          <h2 className="text-3xl font-bold mb-4">คาเฟ่บ้านไม้ใจกลางเมืองเก่า</h2>
          <p className="mb-4">
            โฮมคาเฟ่เล็กๆ ที่ออกแบบสนองความต้องการของเจ้าของบ้านที่ชอบบ้านไม้เป็นทุนเดิมอยู่แล้ว
            เดิมทีเป็นบ้านไม้เก่าของ ตาศรีพรม ที่ได้รับมรดกมาจากขุนเกษม อยากให้ลองแวะมานั่งสัมผัสบรรยากาศบ้านไม้อายุ เกือบ 100 ปี

          </p>
          <p>สไตล์บ้านไม้โบราณผสมความร่วมสมัย ให้เพลิดเพลินกับกลิ่นกาแฟและเพลงแจ๊สเบา ๆ</p>

          {/* แจ้งเตือนถ้ามีภาพเสีย */}
          {badImages.length > 0 && (
            <div className="mt-4 p-3 text-sm bg-red-100 border border-red-300 text-red-800 rounded-lg">
              ⚠️ รูปโหลดไม่สำเร็จ {badImages.length} ไฟล์:
              <ul className="list-disc ml-5">
                {badImages.map((src, i) => (
                  <li key={i}>{src.replace("/images/", "")}</li>
                ))}
              </ul>
              ตรวจสอบว่ามีไฟล์อยู่จริงใน public/images และชื่อไฟล์ตรงตามโค้ด
            </div>
          )}
        </div>
      </section>

      {/* เมนูแนะนำ */}
      <section className="bg-[#f0e8dc] py-12" aria-label="Menu" data-testid="menu">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold mb-8 text-center">เมนูแนะนำ</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { name: "เค้กมัทฉะ", img: "/images/menu-matcha.jpg" },
              { name: "กาแฟซิกเนเจอร์", img: "/images/menu-coffee.jpg" },
              { name: "มัทฉะลาเต้", img: "/images/menu-matcha-latte.jpg" },
            ].map((item, i) => (
              <motion.div
                key={i}
                className="bg-white rounded-xl shadow-lg overflow-hidden"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
              >
                <img
                  src={item.img}
                  alt={`${item.name} - Si-Wara Café คาเฟ่บ้านไม้ ตะกั่วป่า`}
            className="w-full h-96 object-cover"
                />
          <div className="p-6 text-center text-lg font-semibold">{item.name}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ติดต่อ & แผนที่ */}
      <section
        className="py-12 max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-8 items-center"
        aria-label="Contact"
        data-testid="contact"
      >
        <div>
          <h2 className="text-3xl font-bold mb-4">ติดต่อเรา</h2>
          <p className="flex items-center gap-2 mb-2"><Phone size={20}/> 097-350-1514</p>
          <p className="flex items-center gap-2 mb-2"><MapPin size={20}/> 53 ถนน ราษฎร์บำรุง ตำบล บางไทร อำเภอตะกั่วป่า พังงา 82110</p>
          <p>เปิดทุกวัน 10:00 – 17:00 น.</p>
        </div>

        {mapEmbedSrc?.startsWith("https://www.google.com/maps/embed") ? (
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1658.1055435387063!2d98.3628632!3d8.8336595!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3050db365f08d92d%3A0x5402fc40034bbf27!2z4Lio4Li0LeC4p-C4o-C4siDguITguLLguYDguJ_guYgg4LiV4Liw4LiB4Lix4LmI4Lin4Lib4LmI4Liy!5e1!3m2!1sth!2sth!4v1754898851972!5m2!1sth!2sth"
            width="100%"
            height="100%"
            style={{ border: 0 }}
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
        />
        ) : (
          <div className="w-full h-64 rounded-xl border bg-white flex flex-col items-center justify-center gap-3">
            <span>แผนที่จะมาแสดงเมื่อใส่ <code>mapEmbedSrc</code></span>
            <a className="underline" href="https://maps.google.com/?q=Si-Wara+Cafe+Takua+Pa" target="_blank" rel="noreferrer">
              เปิดใน Google Maps
            </a>
          </div>
        )}
      </section>

      <footer className="bg-[#4a3c2a] text-white py-6 text-center">
        <p>© {new Date().getFullYear()} Si-Wara Café | คาเฟ่บ้านไม้ตะกั่วป่า</p>
      </footer>
    </div>
  );
}
