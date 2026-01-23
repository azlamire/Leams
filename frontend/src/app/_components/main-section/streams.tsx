"use client"

import { api } from "@/lib/api";
import Link from "next/link";
import { MAIN } from "@/shared/constants";
import { useEffect, useState, useReducer, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import { MainCategory } from "./category";
import { store } from "@/shared/store";
import { useStore } from "@tanstack/react-store";
export function MainStreams() {
}

