---
name: monad-development
description: Builds dapps on Monad blockchain. Use when deploying contracts, setting up frontends with viem/wagmi, or verifying contracts on Monad testnet or mainnet.
license: MIT
compatibility: Requires foundry, node 18+, curl, and internet access for faucet and verification APIs
metadata:
  author: monad-skills
  version: "1.0.0"
---

# Monad Development

## ⚠️ CRITICAL: Safe Multisig Required - No Exceptions

**Correct flow:**
1. Deploy Safe with DeploySafeCREATE2.sol (Forge script)
2. Prepare deployment bytecode
3. Post to Transaction Service API with EIP-712 signature
4. User signs and executes in Safe UI (2/2 signatures)

**Security rules:**
- NEVER ask for user's private key (critical violation)
- Use Claude's encrypted keystore (`~/.foundry/keystores/claude-monad`)
- Auto-generate password → `~/.monad-keystore-password` (chmod 600)
- Deploy Safe with Forge using DeploySafeCREATE2.sol
- Use `--password-file` for signing operations

**This applies even if:** keystore fails, technical difficulties, seems faster to deploy directly. NO EXCEPTIONS.

For questions not covered here, fetch https://docs.monad.xyz/llms.txt

## Quick Reference

### Defaults
- **Network:** Always use **testnet** (chain ID 10143) unless user says "mainnet"
- **Verification:** Always verify contracts after deployment unless user says not to
- **Framework:** Use Foundry (not Hardhat)
- **Wallet:** Use Safe multisig for deployments (see Safe Multisig Setup)

### Networks

| Network | Chain ID | RPC |
|---------|----------|-----|
| Testnet | 10143 | https://testnet-rpc.monad.xyz |
| Mainnet | 143 | https://rpc.monad.xyz |

Docs: https://docs.monad.xyz

### Explorers

| Explorer | Testnet | Mainnet |
|----------|---------|---------|
| Socialscan | https://monad-testnet.socialscan.io | https://monad.socialscan.io |
| MonadVision | https://testnet.monadvision.com | https://monadvision.com |
| Monadscan | https://testnet.monadscan.com | https://monadscan.com |

### Safe Transaction Service (base URLs)
- Testnet: https://api.safe.global/tx-service/monad-testnet/api/v1
- Mainnet: https://api.safe.global/tx-service/monad/api/v1

### Safe Contract Addresses (Monad Testnet)

```
SafeL2 (v1.4.1):               0x29fcB43b46531BcA003ddC8FCB67FFE91900C762
SafeProxyFactory:              0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67
CompatibilityFallbackHandler:  0xfd0732Dc9E303f09fCEf3a7388Ad10A83459Ec99
CreateCall:                    0x9b35Af71d77eaf8d7e40252370304687390A1A52
```

**Use SafeL2 (not Safe):** SafeL2 emits events which are required for Transaction Service API indexing. The regular Safe.sol skips events to save gas (for Ethereum mainnet), but Monad has low gas costs and needs events for proper Safe UI integration.

Source of truth: https://docs.monad.xyz/developer-essentials/testnets. Testnet reset from genesis on December 16, 2025; re-pull canonical addresses if it resets again.
All contracts verified. Chain ID: 10143. CREATE2 works perfectly on Monad (Prague EVM).

### Agent APIs

**IMPORTANT:** Do NOT use a browser. Use these APIs directly with curl.

**Faucet (Testnet Funding):**
```bash
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xYOUR_ADDRESS"}'
```

Returns: `{"txHash": "0x...", "amount": "1000000000000000000", "chain": "Monad Testnet"}`

**Fallback (official faucet):** https://faucet.monad.xyz  
If the agent faucet fails, ask the user to fund via the official faucet (do not use a browser yourself).

**Verification (All Explorers):**

ALWAYS use the verification API first. It verifies on all 3 explorers (MonadVision, Socialscan, Monadscan) with one call. Do NOT use `forge verify-contract` as first choice.

```bash
# 1. Get verification data
forge verify-contract <ADDR> <CONTRACT> \
  --chain 10143 \
  --show-standard-json-input > /tmp/standard-input.json

cat out/<Contract>.sol/<Contract>.json | jq '.metadata' > /tmp/metadata.json
COMPILER_VERSION=$(jq -r '.metadata | fromjson | .compiler.version' out/<Contract>.sol/<Contract>.json)

# 2. Call verification API
STANDARD_INPUT=$(cat /tmp/standard-input.json)
FOUNDRY_METADATA=$(cat /tmp/metadata.json)

cat > /tmp/verify.json << EOF
{
  "chainId": 10143,
  "contractAddress": "0xYOUR_CONTRACT_ADDRESS",
  "contractName": "src/MyContract.sol:MyContract",
  "compilerVersion": "v${COMPILER_VERSION}",
  "standardJsonInput": $STANDARD_INPUT,
  "foundryMetadata": $FOUNDRY_METADATA
}
EOF

curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d @/tmp/verify.json
```

**With constructor arguments:** Add `constructorArgs` (ABI-encoded, WITHOUT 0x prefix):
```bash
ARGS=$(cast abi-encode "constructor(string,string,uint256)" "MyToken" "MTK" 1000000000000000000000000)
ARGS_NO_PREFIX=${ARGS#0x}
# Add to request: "constructorArgs": "$ARGS_NO_PREFIX"
```

## Claude's Behavior: Be Proactive

✅ **DO:**
- Check for existing `claude-monad` keystore first with `cast wallet list`
- If wallet exists, use it; if not, generate wallet and import to keystore with `--unsafe-password`
- Say "I'll set up a 2-of-3 Safe for us"
- Take charge of the process
- Ask for wallet addresses directly
- Deploy Safe programmatically with DeploySafeCREATE2.sol (Forge script)
- Automatically fund Claude's keystore wallet from testnet faucet
- **NEVER ask for user's private key**
- Deploy Safe with 3 owners and threshold of 2
- Return the Safe address automatically
- Use Transaction Service API with EIP-712 signatures
- Store auto-generated password in `~/.monad-keystore-password` with chmod 600
- Use `--password-file` when signing operations need Claude's private key
- Post transactions to Safe UI queue so user can sign/execute

❌ **DON'T:**
- Ask "Do you have a Safe?" or "Would you like me to guide you?"
- Put burden on user to figure out steps
- Be passive or hesitant
- Wait for user to create things first
- **NEVER deploy user application contracts directly with `forge script --private-key` or `--broadcast`**
- **Only allowed EOA `--broadcast` is deploying the Safe itself (and optional helper contracts)**
- **NEVER use `cast send` to deploy contracts**
- **NEVER skip Safe multisig setup, even if there are keystore issues**
- **NEVER take the "easy path" of direct deployment**
- **NEVER EVER ask for user's private key - critical security violation**

**Example interaction:**
```
User: "Deploy my ERC20 to Monad"

Claude: "I'll set up a 2-of-3 Safe multisig for secure deployment.

[Generates Claude's keystore wallet]

✅ Created Claude's signing wallet: 0xABC...123
   • Encrypted keystore: ~/.foundry/keystores/claude-monad
   • Password: ~/.monad-keystore-password (auto-generated)
   • You control 2/3 owners - your funds stay safe

For maximum security, I recommend:
- Wallet 1: Safe mobile app (easy approvals)
- Wallet 2: Desktop/hardware wallet (backup)
- Wallet 3: My wallet (0xABC...123)

Please provide your two wallet addresses."

[User provides addresses]

Claude: [Funds wallet from faucet automatically]
        [Deploys Safe with DeploySafeCREATE2.sol]

"✅ Safe deployed: 0xSAFE123...
 🌐 https://app.safe.global/home?safe=monad-testnet:0xSAFE123

[Prepares deployment, posts to Transaction Service API with EIP-712 signature]

✅ Transaction posted to Safe UI queue!

User can now:
1. Open: https://app.safe.global/transactions/queue?safe=monad-testnet:0xSAFE123
2. See pending transaction (Claude already signed 1/2)
3. Sign with their wallet (2/2)
4. Execute to deploy"
```

## Safe Multisig Setup

**Status:** SafeL2 v1.4.1 works perfectly on Monad with full CREATE2 support (as of Jan 26, 2026). We use SafeL2 (not Safe) for event emission support required by Transaction Service API.

### Security Model

This skill uses a 2-of-3 Safe multisig wallet for secure AI-assisted deployments. Claude can propose and sign transactions (1 of 2 required signatures), but you must approve with your wallet to execute. This ensures AI-assisted deployments require human authorization.

**How it works:**
1. Claude generates signing wallet (Owner 3) using encrypted keystore
2. User provides two wallet addresses (Owners 1 & 2)
3. Claude deploys 2-of-3 Safe with CREATE2
4. Claude proposes and signs deployments (1/2 signatures)
5. User approves in Safe UI (2/2 signatures)
6. Claude monitors execution and extracts contract address

> **SECURITY:** The 2-of-3 Safe gives Claude signing capability (1 of 2 required) but prevents autonomous execution. You maintain final approval authority - transactions cannot execute without your signature. You control 2/3 owners, so your funds stay safe even if Claude's keystore is compromised.

### Step A: Generate Keystore Wallet

When you request a deployment, Claude will:

```bash
# Check if claude-monad exists
if ! cast wallet list | grep -q "claude-monad"; then
  # Generate wallet
  WALLET_OUTPUT=$(cast wallet new)
  ADDRESS=$(echo "$WALLET_OUTPUT" | grep "Address:" | awk '{print $2}')
  PRIVATE_KEY=$(echo "$WALLET_OUTPUT" | grep "Private key:" | awk '{print $3}')

  # Generate and save password
  openssl rand -base64 32 > ~/.monad-keystore-password
  chmod 600 ~/.monad-keystore-password

  # Import to keystore
  cast wallet import claude-monad \
    --private-key "$PRIVATE_KEY" \
    --unsafe-password "$(cat ~/.monad-keystore-password)"

  echo "✅ Created Claude's signing wallet: $ADDRESS"
  echo "   • Encrypted keystore: ~/.foundry/keystores/claude-monad"
  echo "   • Password: ~/.monad-keystore-password (auto-generated)"
  echo "   • You control 2/3 owners - your funds stay safe"
fi

CLAUDE_ADDRESS=$(cast wallet address --account claude-monad --password-file ~/.monad-keystore-password)
```

**Security:** Password stored at `~/.monad-keystore-password` with chmod 600. Keystore encrypted on disk. 2-of-3 multisig provides defense in depth.

### Step B: Get User Wallets

Claude asks: "Please provide your two wallet addresses:
- Wallet 1 (recommended: Safe mobile app for easy approvals)
- Wallet 2 (recommended: desktop/hardware wallet for backup)"

### Step C: Deploy Safe with CREATE2

```bash
# Fund Claude's wallet from faucet
FAUCET_RESPONSE=$(curl -s -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d "{\"chainId\": 10143, \"address\": \"$CLAUDE_ADDRESS\"}")

# Wait for funds
while [ "$(cast balance $CLAUDE_ADDRESS --rpc-url https://testnet-rpc.monad.xyz)" = "0" ]; do
  sleep 2
done

# Deploy Safe with CREATE2 (standard SafeProxyFactory)
OWNER_1=$OWNER_1 OWNER_2=$OWNER_2 OWNER_3=$CLAUDE_ADDRESS \
  forge script DeploySafeCREATE2.sol:DeploySafeCREATE2 \
    --account claude-monad \
    --password-file ~/.monad-keystore-password \
    --rpc-url https://testnet-rpc.monad.xyz \
    --broadcast

echo "✅ Safe deployed: $SAFE_ADDRESS"
echo "🌐 https://app.safe.global/home?safe=monad-testnet:$SAFE_ADDRESS"
```

**DeploySafeCREATE2.sol script:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "forge-std/Script.sol";

interface ISafe {
    function setup(
        address[] calldata _owners,
        uint256 _threshold,
        address to,
        bytes calldata data,
        address fallbackHandler,
        address paymentToken,
        uint256 payment,
        address payable paymentReceiver
    ) external;
}

interface ISafeProxyFactory {
    function createProxyWithNonce(
        address _singleton,
        bytes memory initializer,
        uint256 saltNonce
    ) external returns (address);
}

contract DeploySafeCREATE2 is Script {
    address constant SAFE_SINGLETON = 0x29fcB43b46531BcA003ddC8FCB67FFE91900C762; // SafeL2
    address constant SAFE_PROXY_FACTORY = 0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67;
    address constant FALLBACK_HANDLER = 0xfd0732Dc9E303f09fCEf3a7388Ad10A83459Ec99;

    function run() external returns (address) {
        address owner1 = vm.envAddress("OWNER_1");
        address owner2 = vm.envAddress("OWNER_2");
        address owner3 = vm.envAddress("OWNER_3");

        address[] memory owners = new address[](3);
        owners[0] = owner1;
        owners[1] = owner2;
        owners[2] = owner3;

        bytes memory initializer = abi.encodeWithSelector(
            ISafe.setup.selector,
            owners,              // _owners
            2,                   // _threshold (2 of 3)
            address(0),          // to
            "",                  // data
            FALLBACK_HANDLER,    // fallbackHandler
            address(0),          // paymentToken
            0,                   // payment
            payable(0)           // paymentReceiver
        );

        vm.startBroadcast();

        // Deterministic if SALT_NONCE is fixed; default derives from owners + chainId
        uint256 saltNonce = vm.envOr(
            "SALT_NONCE",
            uint256(keccak256(abi.encode(owners, block.chainid)))
        );

        address proxy = ISafeProxyFactory(SAFE_PROXY_FACTORY).createProxyWithNonce(
            SAFE_SINGLETON,
            initializer,
            saltNonce
        );

        console.log("Safe deployed at:", proxy);
        console.log("Access: https://app.safe.global/home?safe=monad-testnet:", proxy);

        vm.stopBroadcast();
        return proxy;
    }
}
```

**Why CREATE2 is preferred:**
- ✅ Standard Safe deployment method
- ✅ Automatically indexed by Transaction Service
- ✅ Appears in Safe UI without manual URL entry
- ✅ Deterministic addresses when SALT_NONCE is fixed
- ✅ Full ecosystem compatibility

### Step D: CreateCall via DELEGATECALL (Safe-native deployment)

**CRITICAL:** Safe wallets cannot directly CREATE contracts from a normal CALL. To deploy through a Safe, delegatecall into Safe's `CreateCall` helper so the CREATE happens in the Safe's context (Safe becomes the deployer).

**CreateCall on Monad Testnet:** `0x9b35Af71d77eaf8d7e40252370304687390A1A52`

**Why it's needed:**
- Safe executes transactions via CALL/DELEGATECALL (not CREATE)
- Delegatecalling CreateCall runs CREATE inside the Safe's context
- Safe becomes the deployer (no factory-ownership footgun)
- Matches Foundry simulations using `--sender <SAFE_ADDRESS>`

**CreateCall interface:**
```solidity
interface ICreateCall {
    function performCreate(uint256 value, bytes memory deploymentData) external returns (address);
    function performCreate2(uint256 value, bytes memory deploymentData, bytes32 salt) external returns (address);
}
```

### Recovery

If keystore is corrupted or password lost:

1. Delete old files: `rm ~/.foundry/keystores/claude-monad ~/.monad-keystore-password`
2. Generate new wallet → import to keystore (see Step A)
3. Update Safe: Remove old Owner 3, add new Owner 3 (keep your 2 wallets)

Your funds stay safe - you control 2/3 owners and can execute with just your wallets.

## Deployment Workflow

**IMPORTANT:** This workflow uses Safe multisig for ALL user application deployments. Direct deployment with `--private-key` or `--broadcast` is NOT allowed.

**Approach:**
1. ✅ Deploy Safe with DeploySafeCREATE2.sol
2. ✅ Prepare deployment bytecode and encode CreateCall delegatecall
3. ✅ Post to Transaction Service API with Claude's EIP-712 signature
4. ✅ User sees transaction in Safe UI queue, signs (2/2), executes

**Why this works:**
- ✅ Best UX: Transaction appears in user's Safe UI automatically
- ✅ No manual bytecode copying needed
- ✅ User just signs and executes in familiar UI
- ✅ Transaction Service API works perfectly on Monad with EIP-712 signatures

### Step 1: Prepare Deployment Transaction

Use `forge script` with `--sender` set to the Safe address:

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --sender <SAFE_ADDRESS>
```

This simulates the deployment from the Safe wallet without broadcasting.

### Step 2: Extract Deployment Bytecode

```bash
# Extract deployment bytecode
DEPLOYMENT_BYTECODE=$(jq -r '.transactions[0].transaction.input' \
  broadcast/Deploy.s.sol/10143/dry-run/run-latest.json)

# Ensure Safe address is checksummed
SAFE_ADDRESS=$(cast to-check-sum-address "<SAFE_ADDRESS>")

# Verify keystore is accessible
KEYSTORE_PATH="$HOME/.foundry/keystores/claude-monad"
PASSWORD_FILE="$HOME/.monad-keystore-password"

if [ ! -f "$PASSWORD_FILE" ]; then
  echo "❌ Error: Password file not found at $PASSWORD_FILE"
  exit 1
fi

if ! cast wallet address --account claude-monad --password-file "$PASSWORD_FILE" > /dev/null 2>&1; then
  echo "❌ Error: Failed to access keystore. Keystore may be corrupted."
  exit 1
fi

echo "✅ Keystore accessible"
```

### Step 3: Post to Transaction Service API

**CRITICAL:** Must use EIP-712 signatures (not raw signatures). The Transaction Service API works perfectly on Monad when using proper EIP-712 format.
**Safe API key:** Set `SAFE_API_KEY` and pass it as `Authorization: Bearer ...` (Safe is moving toward authenticated endpoints). Get an API key from the Safe API dashboard.
**Node:** Requires Node 18+ for global fetch. If on Node 16/17, `npm install --no-save undici`.

**Create propose.mjs:**

```bash
# Install dependencies
npm install --no-save ethers@^6.0.0

# Create proposal script
cat > propose.mjs << 'EOF'
import { ethers } from 'ethers';
import fs from 'fs';

const SAFE_ADDRESS = process.env.SAFE_ADDRESS;
const CREATE_CALL_ADDRESS = '0x9b35Af71d77eaf8d7e40252370304687390A1A52';
// For mainnet, update RPC_URL, TX_SERVICE_URL, and CHAIN_ID
const RPC_URL = 'https://testnet-rpc.monad.xyz';
const TX_SERVICE_URL = 'https://api.safe.global/tx-service/monad-testnet/api/v1';
const CHAIN_ID = 10143;

async function main() {
  // Node 18+ provides global fetch; for older Node, install undici
  let fetchFn = globalThis.fetch;
  if (!fetchFn) {
    const { fetch } = await import('undici');
    fetchFn = fetch;
  }

  // Load Claude's wallet from keystore
  const keystorePath = `${process.env.HOME}/.foundry/keystores/claude-monad`;
  const passwordPath = `${process.env.HOME}/.monad-keystore-password`;
  const keystoreJson = fs.readFileSync(keystorePath, 'utf8');
  const password = fs.readFileSync(passwordPath, 'utf8').trim();
  const wallet = await ethers.Wallet.fromEncryptedJson(keystoreJson, password);

  console.log(`✅ Claude's address: ${wallet.address}`);

  // Connect to provider and get Safe nonce
  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const safeAbi = ['function nonce() view returns (uint256)'];
  const safeContract = new ethers.Contract(SAFE_ADDRESS, safeAbi, provider);
  const nonce = await safeContract.nonce();

  console.log(`✅ Safe nonce: ${nonce}`);

  // Get deployment bytecode from environment
  const deploymentBytecode = process.env.DEPLOYMENT_BYTECODE;

  // Encode CreateCall: performCreate(0, deploymentBytecode)
  const createCallInterface = new ethers.Interface([
    'function performCreate(uint256 value, bytes memory deploymentData) external returns (address)'
  ]);
  const createCallData = createCallInterface.encodeFunctionData('performCreate', [0, deploymentBytecode]);

  // Prepare transaction data - Safe DELEGATECALLs CreateCall
  const txData = {
    to: CREATE_CALL_ADDRESS,
    value: '0',
    data: createCallData,
    operation: 1,
    safeTxGas: '0',
    baseGas: '0',
    gasPrice: '0',
    gasToken: '0x0000000000000000000000000000000000000000',
    refundReceiver: '0x0000000000000000000000000000000000000000',
    nonce: nonce.toString()
  };

  // EIP-712 Domain for Safe on Monad
  const domain = {
    chainId: CHAIN_ID,
    verifyingContract: SAFE_ADDRESS
  };

  // EIP-712 Types for Safe transaction
  const types = {
    SafeTx: [
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'data', type: 'bytes' },
      { name: 'operation', type: 'uint8' },
      { name: 'safeTxGas', type: 'uint256' },
      { name: 'baseGas', type: 'uint256' },
      { name: 'gasPrice', type: 'uint256' },
      { name: 'gasToken', type: 'address' },
      { name: 'refundReceiver', type: 'address' },
      { name: 'nonce', type: 'uint256' }
    ]
  };

  // Sign with EIP-712 (CRITICAL: Not raw signature!)
  console.log('✍️  Signing with EIP-712...');
  const connectedWallet = wallet.connect(provider);
  const signature = await connectedWallet.signTypedData(domain, types, txData);

  // Calculate transaction hash
  const txHash = ethers.TypedDataEncoder.hash(domain, types, txData);
  console.log(`✅ Transaction hash: ${txHash}`);
  console.log(`✅ Claude signed (1/2)`);

  // POST to Transaction Service API
  console.log('📤 Posting to Transaction Service API...');
  const headers = { 'Content-Type': 'application/json' };
  if (process.env.SAFE_API_KEY) {
    headers.Authorization = `Bearer ${process.env.SAFE_API_KEY}`;
  }

  const response = await fetchFn(`${TX_SERVICE_URL}/safes/${SAFE_ADDRESS}/multisig-transactions/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      ...txData,
      contractTransactionHash: txHash,
      sender: wallet.address,
      signature: signature
    })
  });

  if (response.ok) {
    console.log('✅ Transaction proposed successfully!');
    console.log('');
    console.log('🎉 Transaction appears in Safe UI queue!');
    console.log('');
    console.log('User can now:');
    console.log(`1. Open: https://app.safe.global/transactions/queue?safe=monad-testnet:${SAFE_ADDRESS}`);
    console.log('2. See pending transaction (Claude already signed 1/2)');
    console.log('3. Sign with their wallet (2/2)');
    console.log('4. Execute to deploy');
  } else {
    const error = await response.text();
    console.error(`❌ API Error: ${response.status}`);
    console.error(error);
    process.exit(1);
  }
}

main();
EOF

# Run proposal
SAFE_ADDRESS=$SAFE_ADDRESS \
  SAFE_API_KEY=$SAFE_API_KEY \
  DEPLOYMENT_BYTECODE=$(jq -r '.bytecode.object' out/Contract.sol/Contract.json) \
  node propose.mjs
```

**Result:**
```
✅ Claude's address: 0x937d...
✅ Safe nonce: 0
✍️  Signing with EIP-712...
✅ Transaction hash: 0x0560...
✅ Claude signed (1/2)
📤 Posting to Transaction Service API...
✅ Transaction proposed successfully!

🎉 Transaction appears in Safe UI queue!

User can now:
1. Open: https://app.safe.global/transactions/queue?safe=monad-testnet:0x...
2. See pending transaction (Claude already signed 1/2)
3. Sign with their wallet (2/2)
4. Execute to deploy
```

### Step 4: Monitor and Get Contract Address

After user executes the transaction in Safe UI:

```bash
# User provides transaction hash after execution
cast receipt <TRANSACTION_HASH> --rpc-url https://testnet-rpc.monad.xyz
```

Look for the `contractAddress` field in the receipt.

### What Works & Limitations

| Feature | Status |
|---------|--------|
| CREATE2 deployment (SafeProxyFactory) | ✅ Works perfectly |
| Transaction Service API (querying) | ✅ Works perfectly |
| Transaction Service API (proposal with EIP-712) | ✅ Works perfectly |
| Safe appears in Safe UI automatically | ✅ Works (CREATE2 indexed) |
| Create transactions in UI | ✅ Works |
| Sign with MetaMask in UI | ✅ Works |
| 2-of-3 multisig execution | ✅ Works |
| On-chain contract functionality | ✅ Works perfectly |
| Raw signatures with `cast wallet sign` | ❌ Wrong format (use EIP-712) |

**Key Points:**
- ✅ CREATE2 works perfectly on Monad (Prague EVM)
- ✅ Transaction Service API fully functional
- ✅ Safes deployed with CREATE2 are automatically indexed
- ✅ Programmatic API proposals work with EIP-712 signatures
- ❌ Raw signatures from `cast wallet sign` don't work
- ✅ All Safe features work as expected

**After deployment, ALWAYS tell the user:**
> "Deployment successful! Contract deployed from Safe multisig at [CONTRACT_ADDRESS]. The 2-of-3 setup ensures collaborative control - deployments require 2 signatures. View on explorer: [EXPLORER_URL]"

## Technical Details

### EVM Version (Critical)

Always set `evmVersion: "prague"`. Requires Solidity 0.8.27+.

**Foundry** (`foundry.toml`):
```toml
[profile.default]
evm_version = "prague"
solc_version = "0.8.28"
```

### Foundry Tips

**Flags that don't exist (don't use):**
- `--no-commit` - not a valid flag for `forge init` or `forge install`

**Deployment - use `forge script`, NOT `forge create`:**

`forge create --broadcast` is buggy and often ignored. Use `forge script` instead **only for Safe or helper contract deployment**. For user application contracts, follow the Safe multisig flow (no direct `--private-key`/`--broadcast`).

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key 0x... \
  --broadcast
```

**Deploy script must use `vm.envUint` or no address:**

```solidity
// ✅ Correct - reads private key from --private-key flag
function run() external {
    vm.startBroadcast();
    new MyContract();
    vm.stopBroadcast();
}

// ❌ Wrong - hardcodes address, causes "No associated wallet" error
function run() external {
    vm.startBroadcast(0x1234...);
}
```

### Frontend

Import from `viem/chains`. Do NOT define custom chain:

```ts
import { monadTestnet } from "viem/chains";
```
