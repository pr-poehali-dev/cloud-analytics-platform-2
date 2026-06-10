import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Layout, Palette, Code, Share2, Target, Search } from "lucide-react"

const services = [
  {
    icon: Layout,
    title: "Веб-дизайн",
    description:
      "Мы создаем сайты, которые не только визуально привлекательны, но и функциональны, удобны в использовании. В CodeCraft ваш бренд в центре внимания — мы обеспечиваем соответствие онлайн-присутствия целям и ценностям вашего бизнеса.",
  },
  {
    icon: Palette,
    title: "Графический дизайн",
    description:
      "От логотипов до постов в соцсетях — мы создаем креативные графические решения, усиливающие ваш бренд. Наши дизайны уникальны и профессиональны, производя нужное впечатление на целевую аудиторию.",
  },
  {
    icon: Code,
    title: "Веб-разработка",
    description:
      "Мы создаем технически надежные и перспективные сайты. Наша команда обеспечивает надежность, масштабируемость и скорость, помогая вашему бизнесу расти в цифровом пространстве.",
  },
  {
    icon: Share2,
    title: "Соцсети",
    description:
      "Сильное присутствие в социальных сетях сегодня решает многое. Мы поможем создать впечатление с помощью привлекательных визуалов и эффективных стратегий, чтобы ваш бренд оставался заметным.",
  },
  {
    icon: Target,
    title: "Результат",
    description:
      "В CodeCraft мы нацелены на успех. Наш подход всегда направлен на достижение измеримых результатов, способствующих росту вашего бизнеса. Вместе находим то, что действительно работает.",
  },
  {
    icon: Search,
    title: "SEO",
    description:
      "Видимость в поиске критически важна. Мы оптимизируем сайт с применением современных SEO-техник, чтобы вы были выше в Google и целевая аудитория легко вас находила.",
  },
]

export function ServicesSection() {
  return (
    <section id="services" className="py-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-primary/5 animate-pulse" />

      <div className="container mx-auto max-w-7xl relative z-10">
        <div className="inline-block mb-4 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-semibold mx-auto block w-fit">
          Наша экспертиза
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center mb-4 text-balance">
          В чем мы <span className="text-primary">сильны</span>
        </h2>
        <p className="text-center text-muted-foreground mb-12 max-w-3xl mx-auto text-pretty leading-relaxed text-lg">
          От концепции до запуска — мы трансформируем ваши цифровые амбиции в мощные онлайн-решения, приносящие результат.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, index) => (
            <Card
              key={index}
              className="group hover:border-primary transition-all duration-300 hover:shadow-xl hover:-translate-y-2 bg-background/50 backdrop-blur-sm"
            >
              <CardHeader>
                <div className="mb-4 inline-flex p-3 rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300 group-hover:scale-110 group-hover:rotate-3">
                  <service.icon className="h-6 w-6" />
                </div>
                <CardTitle className="text-xl group-hover:text-primary transition-colors">{service.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">{service.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
