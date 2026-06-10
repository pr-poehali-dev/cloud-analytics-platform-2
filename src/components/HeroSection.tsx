import { Button } from "@/components/ui/button"
import { ArrowRight, Sparkles, Code2, Palette } from "lucide-react"
import { useEffect, useState } from "react"

export function HeroSection() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center px-4 sm:px-6 lg:px-8 overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div
          className="absolute w-[500px] h-[500px] rounded-full bg-muted/40 blur-3xl animate-pulse"
          style={{
            top: "20%",
            left: "10%",
            animationDuration: "4s",
          }}
        />
        <div
          className="absolute w-[400px] h-[400px] rounded-full bg-muted/30 blur-3xl animate-pulse"
          style={{
            bottom: "10%",
            right: "15%",
            animationDuration: "6s",
            animationDelay: "1s",
          }}
        />
        {/* Subtle mouse-following gradient */}
        <div
          className="absolute w-[300px] h-[300px] rounded-full bg-muted/20 blur-3xl transition-all duration-1000 ease-out"
          style={{
            left: `${mousePosition.x - 150}px`,
            top: `${mousePosition.y - 150}px`,
          }}
        />
      </div>

      <div className="absolute inset-0 pointer-events-none">
        <Code2
          className="absolute text-muted-foreground/30 animate-float"
          style={{
            top: "15%",
            left: "15%",
            animationDelay: "0s",
          }}
          size={40}
        />
        <Palette
          className="absolute text-muted-foreground/30 animate-float"
          style={{
            top: "25%",
            right: "20%",
            animationDelay: "2s",
          }}
          size={35}
        />
        <Sparkles
          className="absolute text-muted-foreground/30 animate-float"
          style={{
            bottom: "20%",
            left: "20%",
            animationDelay: "1s",
          }}
          size={30}
        />
      </div>

      <div className="container mx-auto text-center max-w-5xl relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6 animate-fade-in-up">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium text-primary">Профессиональный веб-дизайн и разработка</span>
        </div>

        <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6 animate-fade-in-up text-balance">
          Сайты, которые{" "}
          <span className="text-primary relative inline-block">
            впечатляют
            <svg
              className="absolute -bottom-2 left-0 w-full"
              height="12"
              viewBox="0 0 200 12"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2 10C50 5 150 5 198 10"
                stroke="currentColor"
                strokeWidth="3"
                strokeLinecap="round"
                className="text-primary"
              />
            </svg>
          </span>
        </h1>

        <p className="text-xl sm:text-2xl text-muted-foreground mb-10 max-w-3xl mx-auto animate-fade-in-up animate-delay-100 leading-relaxed">
          От концепции до запуска. Мы создаем современные, быстрые и результативные сайты, которые выводят ваш бизнес на новый уровень.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fade-in-up animate-delay-200 mb-12">
          <Button
            size="lg"
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold px-8 py-6 text-lg group shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all"
            asChild
          >
            <a href="#contact">
              Начать проект
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </a>
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="border-2 border-primary/20 text-foreground hover:bg-primary/5 hover:border-primary font-semibold px-8 py-6 text-lg backdrop-blur-sm bg-transparent"
            asChild
          >
            <a href="#portfolio">Наши работы</a>
          </Button>
        </div>

        <div className="flex flex-wrap justify-center items-center gap-8 text-sm text-muted-foreground animate-fade-in-up animate-delay-300">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span>50+ проектов</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" style={{ animationDelay: "0.5s" }} />
            <span>45+ довольных клиентов</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" style={{ animationDelay: "1s" }} />
            <span>3+ года опыта</span>
          </div>
        </div>
      </div>
    </section>
  )
}
