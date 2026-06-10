import { Card, CardContent } from "@/components/ui/card"
import { ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"

const projects = [
  {
    title: "Умный помощник по выборам",
    category: "AI/ML и веб-разработка",
    image: "/omgekeerdestemwijzer-banner.png",
    description:
      "AI-приложение для выборов. Пользователи задают вопросы о позициях партий и получают 100% фактические ответы из официальных программ с использованием RAG-технологии.",
    url: "https://de-omgekeerde-stemwijzer.onrender.com/",
    tags: ["Next.js", "AI/ML", "RAG", "TypeScript"],
  },
  {
    title: "Автомойка Tahsin",
    category: "Веб-дизайн и разработка",
    image: "/autopoetsbedrijf-tahsin-project.png",
    description:
      "Профессиональный сайт для автомойки с 20-летним опытом. Полная презентация услуг, автомойки и гаража с современным адаптивным дизайном.",
    url: "https://www.autopoetsbedrijftahsin.nl/",
    tags: ["React", "Next.js", "Tailwind CSS"],
  },
  {
    title: "Кадровое агентство CAN",
    category: "Веб-разработка",
    image: "/can-uitzendbureau-project.png",
    description:
      "Кадровое агентство с 30-летним опытом в садоводческом секторе. Сайт с обзором услуг и прямыми контактами для работодателей и соискателей.",
    url: "https://canbv.nl/",
    tags: ["Next.js", "React", "Tailwind CSS"],
  },
  {
    title: "Портфолио Murat Sahin",
    category: "Портфолио-сайт",
    image: "/murat-sahin-portfolio.png",
    description:
      "Профессиональное портфолио full-stack разработчика. Демонстрация проектов, навыков и опыта с современным минималистичным дизайном и темной темой.",
    url: "https://murat-sahin-dev.vercel.app/",
    tags: ["Next.js", "TypeScript", "Tailwind CSS", ".NET Core"],
  },
]

export function PortfolioSection() {
  return (
    <section id="portfolio" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 text-balance">Наше портфолио</h2>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto text-pretty leading-relaxed">
            Ознакомьтесь с подборкой наших последних проектов и узнайте, как мы помогаем бизнесу расти с помощью мощных цифровых решений.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {projects.map((project, index) => (
            <Card
              key={index}
              className="group overflow-hidden border-none shadow-md hover:shadow-xl transition-all duration-300"
            >
              <div className="relative overflow-hidden aspect-video">
                <img
                  src={project.image || "/placeholder.svg"}
                  alt={project.title}
                  className="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-background/95 via-background/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-6">
                  <Button
                    size="sm"
                    variant="secondary"
                    className="gap-2"
                    onClick={() => window.open(project.url, "_blank")}
                  >
                    Открыть проект <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <CardContent className="p-6">
                <p className="text-sm text-primary font-semibold mb-2">{project.category}</p>
                <h3 className="text-xl font-bold mb-2">{project.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed mb-4">{project.description}</p>
                <div className="flex flex-wrap gap-2">
                  {project.tags.map((tag, tagIndex) => (
                    <span key={tagIndex} className="text-xs px-2 py-1 rounded-full bg-muted text-muted-foreground">
                      {tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
