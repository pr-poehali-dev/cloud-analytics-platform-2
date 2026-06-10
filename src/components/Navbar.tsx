import { ThemeToggle } from "@/components/ThemeToggle"
import { Logo } from "@/components/Logo"
import { MobileMenu } from "@/components/MobileMenu"
import { useState, useEffect } from "react"

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <nav
      className={`sticky top-0 z-50 w-full transition-all duration-300 ${
        isScrolled ? "bg-background/80 backdrop-blur-lg border-b border-border" : "bg-transparent"
      }`}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <a href="/" className="hover:opacity-80 transition-opacity">
            <Logo />
          </a>

          <div className="hidden md:flex items-center gap-8">
            <a href="#about" className="text-sm font-medium hover:text-primary transition-colors">
              О нас
            </a>
            <a href="#services" className="text-sm font-medium hover:text-primary transition-colors">
              Услуги
            </a>
            <a href="#portfolio" className="text-sm font-medium hover:text-primary transition-colors">
              Портфолио
            </a>
            <a href="#pricing" className="text-sm font-medium hover:text-primary transition-colors">
              Тарифы
            </a>
            <a href="#contact" className="text-sm font-medium hover:text-primary transition-colors">
              Контакты
            </a>
          </div>

          <div className="flex items-center gap-2">
            <ThemeToggle />
            <MobileMenu />
          </div>
        </div>
      </div>
    </nav>
  )
}
