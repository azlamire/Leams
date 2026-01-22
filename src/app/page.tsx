"use client"

import { api } from "@/lib/api";
import Link from "next/link";
import { MAIN } from "@/shared/constants";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import { MainCategory } from "./_components/main-section/category";
import { MainStreams } from "./_components/main-section/streams";
export default function MainPage() {
	return (
		<main className="w-full z-0">
			<MainStreams />
		</main>
	)
}
