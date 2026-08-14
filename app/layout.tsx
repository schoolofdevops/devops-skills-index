import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://skills.schoolofdevops.com"),
  title: "DevOps Skills Index 2026",
  description: "A living, evidence-led view of the roles and skills employers ask for across DevOps, platform engineering, SRE and AI operations.",
  openGraph: {
    title: "DevOps Skills Index 2026",
    description: "What does an operations engineer need to know now?",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "DevOps Skills Index 2026" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "DevOps Skills Index 2026",
    description: "What does an operations engineer need to know now?",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className={`${geistSans.variable} ${geistMono.variable}`}>{children}</body></html>;
}
