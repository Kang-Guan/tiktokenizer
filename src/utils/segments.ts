import { type Tiktoken } from "@dqbd/tiktoken";
import Graphemer from "graphemer";

const textDecoder = new TextDecoder();
const graphemer = new Graphemer();

export function getSegments(encoder: Tiktoken, inputText: string) {
  const encoding = encoder.encode(inputText, "all");
  const segments: { text: string; tokens: { id: number; idx: number }[] }[] =
    [];

  let byteAcc: number[] = [];
  let tokenAcc: { id: number; idx: number }[] = [];
  let inputGraphemes = graphemer.splitGraphemes(inputText);

  for (let idx = 0; idx < encoding.length; idx++) {
    const token = encoding[idx]!;
    byteAcc.push(...encoder.decode_single_token_bytes(token));
    tokenAcc.push({ id: token, idx });

    const segmentText = textDecoder.decode(new Uint8Array(byteAcc));
    const graphemes = graphemer.splitGraphemes(segmentText);

    // 关于这段的注释：
    // 有的字符会被解释成多个 token，比如 emoji，这段需要将多个 token 拼接成一个字符
    if (graphemes.every((item, idx) => inputGraphemes[idx] === item)) {
      segments.push({ text: segmentText, tokens: tokenAcc });

      byteAcc = [];
      tokenAcc = [];
      inputGraphemes = inputGraphemes.slice(graphemes.length);
    }
  }
  return segments;
}

// 远程版本
const END_POINT = 'http://localhost:8231/encode'
export type Segments = { text: string; tokens: { id: number; idx: number }[] }[]
export async function getSegmentsFromRemote(encoderName: string, inputText: string): Promise<Segments> {
  const ret = await fetch(END_POINT, {
    method: 'POST',
    body: JSON.stringify({ encoder: encoderName, text: inputText }),
    headers: { 'Content-Type': 'application/json' }
  })
  const json = await ret.json()
  return json as Segments
}