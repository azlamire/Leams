The full overview what's going on frontend part of [Leams](http://localhost:8001/)

## **Structure**
``` { .sh .no-copy }
Leams-frontend/
├─ docs/                    # Auto-generated TypeDoc documentation
│
├─ legacy/                  # Deprecated code and migration guides
│
└─ src/                     # Main source directory
   ├─ app/                  # Next.js App Router pages and layouts
   ├─ configs/              # Configuration files
   ├─ features/             # Feature-based modules
   ├─ hooks/                # Custom React hooks
   ├─ lib/                  # Third-party integrations and utilities
   ├─ shared/               # Shared utilities and constants
   ├─ ui/                   # Reusable UI components
   └─ test/                 # Testing utilities and setup
```

## **Tech Stack**
| Category | Technology | Description |
| -------- | ---------- | ----------- |
| **Framework** | [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Next.js](https://nextjs.org/) | Modern UI framework with strong type safety and server-side rendering features. |
| **Build Tool** | [Bun](https://bun.com/) | Ultra-fast JavaScript runtime and bundle tool for speedy builds.|
| **Styling** | [Tailwind CSS](https://tailwindcss.com/) + [Framer Motion](https://motion.dev/)| Utility-first CSS with robust animation library for smooth, interactive UI. | 
| **State Management** | [TanStack Store](https://tanstack.com/store/latest/docs) | Minimal and powerful global state management. |
| **HTTP Client** | [Axios](https://axios-http.com/) + [TanStack Query](https://tanstack.com/query/docs) | Reliable HTTP client and smart data fetching/caching utilities. |
| **Protocols** | [WebRTC](https://webrtc.org) + [HLS](https://github.com/video-dev/hls.js/) + [obs-websocket-js](https://www.npmjs.com/package/obs-websocket-js) | Real-time communication, streaming video, and OBS studio remote control. |
| **Testing** | [React Testing Library](https://testing-library.com/) + [Playwright](https://playwright.dev/)| Modern testing solutions for components and end-to-end coverage. |
| **Documentation** | [TypeDoc](https://typedoc.org/) | Automated generation of comprehensive code documentation. |

