import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Script from "next/script";
import "./globals.css";
import { NewsProvider } from "@/contexts/NewsContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "🔒 Cyber Security News",
  description: "Stay informed with the latest cybersecurity threats and news",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        {/* Google Analytics */}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-BR9KWY2Y69"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-BR9KWY2Y69');
          `}
        </Script>
      </head>
      <body className={inter.className}>
        <NewsProvider>
          {children}
        </NewsProvider>
      </body>
    </html>
  );
}
