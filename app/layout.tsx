import type { Metadata } from "next";
import "./globals.css";
import Script from "next/script";

export const metadata: Metadata = {
  title: "Si-Wara Café | คาเฟ่บ้านไม้ ตะกั่วป่า",
  description: "Si-Wara Café คาเฟ่บ้านไม้ใจกลางเมืองเก่าตะกั่วป่า เสิร์ฟกาแฟและเค้กโฮมเมด",
  keywords: ["Si-Wara Café","คาเฟ่บ้านไม้","ตะกั่วป่า","คาเฟ่พังงา"],
  metadataBase: new URL("https://www.siwara-cafe.com"),
  alternates: { canonical: "https://www.siwara-cafe.com" },
  openGraph: {
    type: "website",
    title: "Si-Wara Café | คาเฟ่บ้านไม้ ตะกั่วป่า",
    description: "คาเฟ่บ้านไม้ใจกลางเมืองเก่าตะกั่วป่า",
    images: ["/images/siwara-hero.jpg"],
    url: "https://www.siwara-cafe.com",
  },
};

const schema = {
  "@context": "https://schema.org",
  "@type": "CafeOrCoffeeShop",
  name: "Si-Wara Café",
  image: "/images/siwara-hero.jpg",
  address: {
    "@type": "PostalAddress",
    streetAddress: "เลขที่ 88 ถนนศรีตะกั่วป่า",
    addressLocality: "ตะกั่วป่า",
    addressRegion: "พังงา",
    postalCode: "82110",
    addressCountry: "TH",
  },
  telephone: "081-234-5678",
  servesCuisine: ["Coffee","Cake"],
  openingHours: "Mo-Su 09:00-18:00",
  url: "https://www.siwara-cafe.com",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>
        <Script id="ld-json-siwara" type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
        {children}
      </body>
    </html>
  );
}
