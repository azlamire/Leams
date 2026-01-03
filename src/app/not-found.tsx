import Link from 'next/link'


// TODO: Use here the link from mui 'case of the race
export default function NotFound() {
	return (
		<div className="flex justify-center items-center w-full flex-col">
			<h2>Warning this page ain't found</h2>
			<Link href="/" className="text-leams">Return Home</Link>
		</div>
	)
}
