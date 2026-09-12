import { useNavigate } from "react-router-dom"
import { GlassCard } from "@/components/quantum-ui"
import { Button } from "@/components/ui/button"
import {
  Atom,
  Brain,
  GitBranch,
  Network,
  Search,
  Shuffle,
  Waves,
} from "lucide-react"

const algorithms = [
  {
    name: "Superposition",
    difficulty: "Beginner",
    icon: Atom,
    description:
      "Learn how a qubit can exist in a combination of |0⟩ and |1⟩ states.",
  },
  {
    name: "Bell State",
    difficulty: "Beginner",
    icon: Network,
    description:
      "Create two entangled qubits and explore correlated measurement results.",
  },
  {
    name: "GHZ State",
    difficulty: "Intermediate",
    icon: GitBranch,
    description:
      "Build a multi-qubit entangled state using H and controlled-X gates.",
  },
  {
    name: "Quantum Teleportation",
    difficulty: "Intermediate",
    icon: Shuffle,
    description:
      "Explore how an unknown quantum state can be transferred using entanglement.",
  },
  {
    name: "Deutsch Algorithm",
    difficulty: "Intermediate",
    icon: Brain,
    description:
      "Understand how a quantum algorithm can determine a function property efficiently.",
  },
  {
    name: "Grover's Algorithm",
    difficulty: "Advanced",
    icon: Search,
    description:
      "Explore quantum search and amplitude amplification.",
  },
  {
    name: "Quantum Fourier Transform",
    difficulty: "Advanced",
    icon: Waves,
    description:
      "Learn the quantum version of the Fourier transform used in many quantum algorithms.",
  },
]

export default function Algorithms() {
  const navigate = useNavigate()

  const handleTry = (name: string) => {
    if (name === "Superposition") {
      navigate("/lab", {
        state: {
          algorithm: "superposition",
        },
      })
      return
    }

    if (name === "Bell State") {
      navigate("/lab", {
        state: {
          algorithm: "bell",
        },
      })
      return
    }

    if (name === "GHZ State") {
      navigate("/lab", {
        state: {
          algorithm: "ghz",
        },
      })
      return
    }

    navigate("/lab")
  }

  return (
    <div className="min-h-screen space-y-8 p-6 lg:p-8">
      {/* HEADER */}
      <div>
        <div className="mb-2 flex items-center gap-3">
          <Atom className="size-7 text-primary" />
          <h1 className="text-3xl font-bold tracking-tight">
            Quantum Algorithms
          </h1>
        </div>

        <p className="max-w-2xl text-muted-foreground">
          Explore important quantum algorithms, understand how they work,
          and experiment with them in the Circuit Lab.
        </p>
      </div>

      {/* ALGORITHM GRID */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {algorithms.map((algorithm) => {
          const Icon = algorithm.icon

          return (
            <GlassCard
              key={algorithm.name}
              className="flex min-h-[270px] flex-col justify-between p-6 transition-all duration-300 hover:-translate-y-1 hover:border-primary/40"
            >
              <div>
                <div className="mb-5 flex items-start justify-between">
                  <div className="flex size-12 items-center justify-center rounded-xl bg-primary/10">
                    <Icon className="size-6 text-primary" />
                  </div>

                  <span className="rounded-full bg-secondary px-3 py-1 text-xs font-medium">
                    {algorithm.difficulty}
                  </span>
                </div>

                <h2 className="mb-3 text-xl font-semibold">
                  {algorithm.name}
                </h2>

                <p className="text-sm leading-6 text-muted-foreground">
                  {algorithm.description}
                </p>
              </div>

              <Button
                className="mt-6 w-full"
                onClick={() => handleTry(algorithm.name)}
              >
                Try it
              </Button>
            </GlassCard>
          )
        })}
      </div>
    </div>
  )
}
