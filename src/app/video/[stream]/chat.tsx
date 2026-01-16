import { useEffect, useState } from "react";
export function Chat() {
	useEffect(() => {
		const ws = new WebSocket("ws://localhost:8000/video/chat")
		ws.onmessage = (event) => { console.log(event.data) }
		setWs(ws)
		return () => {
			ws?.close()
			setWs(undefined)
		}
	}, [])
	const [ws, setWs] = useState<WebSocket>()
	useEffect(() => {
		console.log(ws)
	}, [ws])
	const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
		if (event.key === 'Enter' && ws !== undefined) {
			console.log("Frontend part: ", event.currentTarget.value)
			ws.send(event.currentTarget.value);
			event.currentTarget.value = ""
			event.preventDefault()
		}
	};

	return (
		<div className="flex-1 flex flex-col">
			<div className="flex-1 flex">
			</div>
			<div className="flex justify-center">
				<input
					className="w-[80%] rounded-full border-2 border-leams "
					onKeyDown={handleKeyDown}
				/>
			</div>
		</div>
	)

}
