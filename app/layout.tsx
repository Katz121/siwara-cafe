import type { Metadata } from "next";
import "./globals.css";
import Script from "next/script";

const SITE_URL = "https://www.siwara.cafe";
const OG_IMAGE = `${SITE_URL}/images/siwara-hero.jpg`; // แก้เป็นภาพ OG ของจริงได้

export const metadata: Metadata = {
  title: "Si-Wara Café | คาเฟ่บ้านไม้ ตะกั่วป่า",
  description:
    "Si-Wara Café คาเฟ่บ้านไม้ใจกลางเมืองเก่าตะกั่วป่า เสิร์ฟกาแฟและเค้กโฮมเมด บรรยากาศอบอุ่นเหมือนอยู่บ้าน",
  keywords: ["Si-Wara Café", "คาเฟ่บ้านไม้", "ตะกั่วป่า", "คาเฟ่พังงา", "เมืองเก่าตะกั่วป่า"],
  metadataBase: new URL(SITE_URL),
  alternates: { canonical: SITE_URL },

  openGraph: {
    type: "website",
    url: SITE_URL,
    title: "Si-Wara Café | คาเฟ่บ้านไม้ ตะกั่วป่า",
    description:
      "Si-Wara Café คาเฟ่บ้านไม้ใจกลางเมืองเก่าตะกั่วป่า เสิร์ฟกาแฟคุณภาพและเค้กโฮมเมด",
    images: [
      {
        url: OG_IMAGE,
        width: 1200,
        height: 630,
        alt: "Si-Wara Café — คาเฟ่บ้านไม้ ตะกั่วป่า",
      },
    ],
    locale: "th_TH",
    siteName: "Si-Wara Café",
  },

  twitter: {
    card: "summary_large_image",
    title: "Si-Wara Café | คาเฟ่บ้านไม้ ตะกั่วป่า",
    description:
      "คาเฟ่บ้านไม้ใจกลางเมืองเก่าตะกั่วป่า เสิร์ฟกาแฟและเค้กโฮมเมด",
    images: [OG_IMAGE],
  },

  // ถ้ามีไฟล์ไอคอน/manifest ใน public/ ใส่ไว้จะดี
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

// ---------- JSON-LD (Local Business / Cafe) ----------
const schema = {
  "@context": "https://schema.org",
  "@type": "CafeOrCoffeeShop",
  "@id": `${SITE_URL}#cafe`,
  name: "Si-Wara Café",
  url: SITE_URL,
  image: `${SITE_URL}/images/siwara-hero.jpg`,
  telephone: "+66-97-350-1514",
  priceRange: "฿฿",
  servesCuisine: ["Coffee", "Cake", "Bakery"],
  address: {
    "@type": "PostalAddress",
    streetAddress: "53 ถนน ราษฎร์บำรุง ตำบล บางไทร",
    addressLocality: "ตะกั่วป่า",
    addressRegion: "พังงา",
    postalCode: "82110",
    addressCountry: "TH",
  },
  geo: {
    "@type": "GeoCoordinates",
    latitude: 8.8336595,
    longitude: 98.3628632,
  },
  openingHoursSpecification: [
    {
      "@type": "OpeningHoursSpecification",
      dayOfWeek: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
      opens: "10:00",
      closes: "17:00",
    },
  ],
  // ใส่ลิงก์โซเชียลของจริงถ้ามี (ช่วย E-E-A-T/Brand)
  sameAs: [
    "https://www.facebook.com/yourpage",
    "https://www.instagram.com/yourpage",
    // "https://maps.app.goo.gl/DJpEqhqui9RUKfKT8"
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>
        {/* GA4 — ใส่ Measurement ID จริงแทน G-XXXXXXX */}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"
          strategy="afterInteractive"
        />
        <Script id="ga4" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-XXXXXXX', { anonymize_ip: true });
          `}
        </Script>

        {/* JSON-LD */}
        <Script
          id="ld-json-cafe"
          type="application/ld+json"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />

        {children}
      </body>
    </html>
  );
}
